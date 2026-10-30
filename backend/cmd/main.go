// cmd/server/main.go
package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"net/url"
	"squad44-backend/internal/config"
	"squad44-backend/model"

	"github.com/jackc/pgx/v5/pgxpool"
)

type HealthResponse struct {
	Status string `json:"status"`
}

type HelloResponse struct {
	Message string `json:"message"`
}

type WeatherResponse struct {
	City        string  `json:"city"`
	Temp        float64 `json:"temp"`
	Description string  `json:"description"`
}

func main() {
	mux := http.NewServeMux()

	// loads config from .env
	cfg, err := config.Load()
	if err != nil {
		log.Fatal(err)
	}

	// connects to postgres pool with pgxpool (https://pkg.go.dev/github.com/jackc/pgx/v5/pgxpool)
	pool, err := pgxpool.New(context.Background(), cfg.DatabaseURL())
	if err != nil {
		log.Fatalf("creating db pool: %v", err)
	}

	// ping db with long standing context (context.Background()) because no context is passed in (no req)
	if err := pool.Ping(context.Background()); err != nil {
		log.Fatalf("db unreachable: %v", err)
	}

	log.Println("Connected to db!")

	// Define an endpoint
	mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(HelloResponse{Message: "Hello World!"})
	})

	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(HealthResponse{Status: "OK"})
	})

	// test api for db
	mux.HandleFunc("GET /api/db-ping", func(w http.ResponseWriter, r *http.Request) {
		println("Pinging database...")
		w.Header().Set("Content-Type", "application/json")
		// when pinging, passes in context of req so is active for duration of req, stops when client exits page
		if err := pool.Ping(r.Context()); err != nil {
			w.WriteHeader(http.StatusServiceUnavailable)
			json.NewEncoder(w).Encode(HealthResponse{Status: "DB unreachable: " + err.Error()})
			return
		}
		json.NewEncoder(w).Encode(HealthResponse{Status: "DB OK"})
	})

	mux.HandleFunc("GET /api/menu-items", func(w http.ResponseWriter, r *http.Request) {
		println("Fetching menu items from database...")
		w.Header().Set("Content-Type", "application/json")
		rows, err := pool.Query(r.Context(), "SELECT menu_item_id, menu_item_name, price FROM menu_items")
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(HealthResponse{Status: "Error fetching menu items: " + err.Error()})
			return
		}
		defer rows.Close()

		var menuItems []model.MenuItem
		for rows.Next() {
			var item model.MenuItem
			if err := rows.Scan(&item.Menu_item_id, &item.Menu_item_name, &item.Price); err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				json.NewEncoder(w).Encode(HealthResponse{Status: "Error scanning menu item: " + err.Error()})
				return
			}
			menuItems = append(menuItems, item)
		}

		if err := rows.Err(); err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(HealthResponse{Status: "Error iterating over menu items: " + err.Error()})
			return
		}

		json.NewEncoder(w).Encode(menuItems)
	})

	mux.HandleFunc("GET /api/menu-items/{id}", func(w http.ResponseWriter, r *http.Request) {
		println("Fetching menu item by ID from database...")
		w.Header().Set("Content-Type", "application/json")
		id := r.PathValue("id")
		var item model.MenuItem
		err := pool.QueryRow(r.Context(), "SELECT menu_item_id, menu_item_name, price FROM menu_items WHERE menu_item_id = $1", id).Scan(&item.Menu_item_id, &item.Menu_item_name, &item.Price)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(HealthResponse{Status: "Error fetching menu item: " + err.Error()})
			return
		}
		json.NewEncoder(w).Encode(item)
	})

	// current weather via OpenWeatherMap, ?city= defaults to College Station
	mux.HandleFunc("GET /api/weather", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if cfg.WeatherAPIKey == "" {
			w.WriteHeader(http.StatusServiceUnavailable)
			json.NewEncoder(w).Encode(HealthResponse{Status: "WEATHER_API not set"})
			return
		}
		city := r.URL.Query().Get("city")
		if city == "" {
			city = "College Station"
		}
		q := url.Values{"q": {city}, "appid": {cfg.WeatherAPIKey}, "units": {"imperial"}}
		req, err := http.NewRequestWithContext(r.Context(), "GET", "https://api.openweathermap.org/data/2.5/weather?"+q.Encode(), nil)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(HealthResponse{Status: "Error building weather request: " + err.Error()})
			return
		}
		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			w.WriteHeader(http.StatusBadGateway)
			json.NewEncoder(w).Encode(HealthResponse{Status: "Error fetching weather: " + err.Error()})
			return
		}
		defer resp.Body.Close()
		if resp.StatusCode != http.StatusOK {
			w.WriteHeader(http.StatusBadGateway)
			json.NewEncoder(w).Encode(HealthResponse{Status: "Weather API returned " + resp.Status})
			return
		}

		var owm struct {
			Name string `json:"name"`
			Main struct {
				Temp float64 `json:"temp"`
			} `json:"main"`
			Weather []struct {
				Description string `json:"description"`
			} `json:"weather"`
		}
		if err := json.NewDecoder(resp.Body).Decode(&owm); err != nil {
			w.WriteHeader(http.StatusBadGateway)
			json.NewEncoder(w).Encode(HealthResponse{Status: "Error decoding weather: " + err.Error()})
			return
		}
		out := WeatherResponse{City: owm.Name, Temp: owm.Main.Temp}
		if len(owm.Weather) > 0 {
			out.Description = owm.Weather[0].Description
		}
		json.NewEncoder(w).Encode(out)
	})

	// Start server on port 8080
	log.Println("Server running on port 8080...")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(http.ListenAndServe(":8080", mux))
	}
}
