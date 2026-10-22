// cmd/server/main.go
package main

import (
	"encoding/json"
	"net/http"
)

type HealthResponse struct {
	Status string `json:"status"`
}

func main() {
	mux := http.NewServeMux()

	// Define an endpoint
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder((w)).Encode(HealthResponse{Status: "OK"})
	})

	// Start server on port 8080
	print("Server running on port 8080...\n")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		panic(err)
	}
}
