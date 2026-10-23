// cmd/server/main.go
package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type HealthResponse struct {
	Status string `json:"status"`
}

type HelloResponse struct {
	Message string `json:"message"`
}

func main() {
	mux := http.NewServeMux()

	// Define an endpoint
	mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(HelloResponse{Message: "Hello World!"})
	})

	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder((w)).Encode(HealthResponse{Status: "OK"})
	})

	// Start server on port 8080
	log.Println("Server running on port 8080...\n")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(http.ListenAndServe(":8080", mux))
	}
}
