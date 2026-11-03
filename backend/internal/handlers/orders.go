package handlers

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"net/http"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

// maxLineQuantity guards against fat-fingered quantities on the touch screen.
const maxLineQuantity = 99

type OrderLine struct {
	MenuItemID int `json:"menu_item_id"`
	Quantity   int `json:"quantity"`
}

type OrderRequest struct {
	EmployeeID int         `json:"employee_id"`
	Tip        float64     `json:"tip"`
	Items      []OrderLine `json:"items"`
}

type OrderResponse struct {
	SaleID   int       `json:"sale_id"`
	SaleDate time.Time `json:"sale_date"`
	Subtotal float64   `json:"subtotal"`
	Tip      float64   `json:"tip"`
}

type errorResponse struct {
	Error string `json:"error"`
}

// errBadOrder marks errors caused by the client's request (-> 400).
var errBadOrder = errors.New("bad order")

// normalizeOrder validates the request and merges duplicate menu items,
// preserving the order in which items were first added.
func normalizeOrder(req OrderRequest) ([]OrderLine, error) {
	if req.EmployeeID <= 0 {
		return nil, fmt.Errorf("%w: employee_id is required", errBadOrder)
	}
	if req.Tip < 0 || math.IsNaN(req.Tip) || math.IsInf(req.Tip, 0) {
		return nil, fmt.Errorf("%w: tip must be a non-negative number", errBadOrder)
	}
	if len(req.Items) == 0 {
		return nil, fmt.Errorf("%w: order has no items", errBadOrder)
	}

	index := map[int]int{}
	var lines []OrderLine
	for _, it := range req.Items {
		if it.Quantity <= 0 || it.Quantity > maxLineQuantity {
			return nil, fmt.Errorf("%w: quantity for item %d must be 1-%d", errBadOrder, it.MenuItemID, maxLineQuantity)
		}
		if i, ok := index[it.MenuItemID]; ok {
			lines[i].Quantity += it.Quantity
			if lines[i].Quantity > maxLineQuantity {
				return nil, fmt.Errorf("%w: quantity for item %d must be 1-%d", errBadOrder, it.MenuItemID, maxLineQuantity)
			}
			continue
		}
		index[it.MenuItemID] = len(lines)
		lines = append(lines, it)
	}
	return lines, nil
}

func roundCents(v float64) float64 {
	return math.Round(v*100) / 100
}

// CreateOrder handles POST /api/orders. Prices come from the database, never
// the client. The sale, its line items, and the inventory deduction are
// written in one transaction so reports and inventory always agree.
func CreateOrder(pool *pgxpool.Pool) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")

		var req OrderRequest
		if err := json.NewDecoder(http.MaxBytesReader(w, r.Body, 1<<16)).Decode(&req); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON: "+err.Error())
			return
		}
		lines, err := normalizeOrder(req)
		if err != nil {
			writeError(w, http.StatusBadRequest, err.Error())
			return
		}

		resp, err := insertOrder(r.Context(), pool, req.EmployeeID, roundCents(req.Tip), lines)
		if errors.Is(err, errBadOrder) {
			writeError(w, http.StatusBadRequest, err.Error())
			return
		}
		if err != nil {
			writeError(w, http.StatusInternalServerError, "error saving order: "+err.Error())
			return
		}

		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(resp)
	}
}

func insertOrder(ctx context.Context, pool *pgxpool.Pool, employeeID int, tip float64, lines []OrderLine) (OrderResponse, error) {
	var resp OrderResponse

	tx, err := pool.Begin(ctx)
	if err != nil {
		return resp, err
	}
	defer tx.Rollback(ctx)

	var exists bool
	if err := tx.QueryRow(ctx, "SELECT EXISTS(SELECT 1 FROM employees WHERE employee_id = $1)", employeeID).Scan(&exists); err != nil {
		return resp, err
	}
	if !exists {
		return resp, fmt.Errorf("%w: unknown employee %d", errBadOrder, employeeID)
	}

	ids := make([]int, len(lines))
	for i, l := range lines {
		ids[i] = l.MenuItemID
	}
	prices := map[int]float64{}
	rows, err := tx.Query(ctx, "SELECT menu_item_id, price::float8 FROM menu_items WHERE menu_item_id = ANY($1)", ids)
	if err != nil {
		return resp, err
	}
	for rows.Next() {
		var id int
		var price float64
		if err := rows.Scan(&id, &price); err != nil {
			rows.Close()
			return resp, err
		}
		prices[id] = price
	}
	rows.Close()
	if err := rows.Err(); err != nil {
		return resp, err
	}

	var subtotal float64
	for _, l := range lines {
		price, ok := prices[l.MenuItemID]
		if !ok {
			return resp, fmt.Errorf("%w: unknown menu item %d", errBadOrder, l.MenuItemID)
		}
		subtotal += price * float64(l.Quantity)
	}
	subtotal = roundCents(subtotal)

	// sale_id is a plain int (not an identity column) because the table is
	// seeded with explicit ids, so serialize id allocation with a table lock.
	if _, err := tx.Exec(ctx, "LOCK TABLE sales IN SHARE ROW EXCLUSIVE MODE"); err != nil {
		return resp, err
	}
	if err := tx.QueryRow(ctx, "SELECT COALESCE(MAX(sale_id), 0) + 1 FROM sales").Scan(&resp.SaleID); err != nil {
		return resp, err
	}
	if err := tx.QueryRow(ctx,
		"INSERT INTO sales (sale_id, sale_date, sale_price, sale_tip, sale_employee_id) VALUES ($1, NOW(), $2, $3, $4) RETURNING sale_date",
		resp.SaleID, subtotal, tip, employeeID,
	).Scan(&resp.SaleDate); err != nil {
		return resp, err
	}

	batch := &pgx.Batch{}
	for _, l := range lines {
		batch.Queue(
			"INSERT INTO sale_menu_items (sale_id, menu_item_id, quantity, price_at_purchase) VALUES ($1, $2, $3, $4)",
			resp.SaleID, l.MenuItemID, l.Quantity, prices[l.MenuItemID],
		)
		// Same clamp-at-zero rule the seed script uses for on-hand inventory.
		batch.Queue(
			`UPDATE supplies s SET quantity = GREATEST(0, s.quantity - mis.quantity * $2)
			 FROM menu_item_supplies mis
			 WHERE mis.supply_id = s.supply_id AND mis.menu_item_id = $1`,
			l.MenuItemID, l.Quantity,
		)
	}
	if err := tx.SendBatch(ctx, batch).Close(); err != nil {
		return resp, err
	}

	if err := tx.Commit(ctx); err != nil {
		return resp, err
	}
	resp.Subtotal = subtotal
	resp.Tip = tip
	return resp, nil
}

type Employee struct {
	EmployeeID int    `json:"employee_id"`
	FirstName  string `json:"first_name"`
	LastName   string `json:"last_name"`
	Role       string `json:"role"`
}

// ListEmployees handles GET /api/employees. It never returns password hashes.
// Used by the cashier screen to attribute sales until login is wired up.
func ListEmployees(pool *pgxpool.Pool) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		rows, err := pool.Query(r.Context(),
			"SELECT employee_id, first_name, last_name, employee_role FROM employees ORDER BY employee_id")
		if err != nil {
			writeError(w, http.StatusInternalServerError, "error fetching employees: "+err.Error())
			return
		}
		employees, err := pgx.CollectRows(rows, func(row pgx.CollectableRow) (Employee, error) {
			var e Employee
			err := row.Scan(&e.EmployeeID, &e.FirstName, &e.LastName, &e.Role)
			return e, err
		})
		if err != nil {
			writeError(w, http.StatusInternalServerError, "error reading employees: "+err.Error())
			return
		}
		json.NewEncoder(w).Encode(employees)
	}
}

func writeError(w http.ResponseWriter, status int, msg string) {
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(errorResponse{Error: msg})
}
