package handlers

import (
	"reflect"
	"testing"
)

func TestNormalizeOrder(t *testing.T) {
	tests := []struct {
		name    string
		req     OrderRequest
		want    []OrderLine
		wantErr bool
	}{
		{
			name: "merges duplicate items and keeps first-seen order",
			req: OrderRequest{EmployeeID: 4, Items: []OrderLine{
				{MenuItemID: 3, Quantity: 1},
				{MenuItemID: 1, Quantity: 2},
				{MenuItemID: 3, Quantity: 2},
			}},
			want: []OrderLine{{MenuItemID: 3, Quantity: 3}, {MenuItemID: 1, Quantity: 2}},
		},
		{name: "rejects empty order", req: OrderRequest{EmployeeID: 4}, wantErr: true},
		{name: "rejects missing employee", req: OrderRequest{Items: []OrderLine{{MenuItemID: 1, Quantity: 1}}}, wantErr: true},
		{name: "rejects zero quantity", req: OrderRequest{EmployeeID: 4, Items: []OrderLine{{MenuItemID: 1, Quantity: 0}}}, wantErr: true},
		{name: "rejects absurd quantity", req: OrderRequest{EmployeeID: 4, Items: []OrderLine{{MenuItemID: 1, Quantity: 1000}}}, wantErr: true},
		{name: "rejects negative tip", req: OrderRequest{EmployeeID: 4, Tip: -1, Items: []OrderLine{{MenuItemID: 1, Quantity: 1}}}, wantErr: true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := normalizeOrder(tt.req)
			if tt.wantErr {
				if err == nil {
					t.Fatalf("expected error, got %v", got)
				}
				return
			}
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Fatalf("got %v, want %v", got, tt.want)
			}
		})
	}
}

func TestRoundCents(t *testing.T) {
	if got := roundCents(5.25*3 + 0.1); got != 15.85 {
		t.Fatalf("got %v, want 15.85", got)
	}
}
