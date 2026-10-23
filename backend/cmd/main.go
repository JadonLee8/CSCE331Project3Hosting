// cmd/server/main.go
package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"squad44-backend/internal/config"

	"github.com/jackc/pgx/v5/pgxpool"
)

type HealthResponse struct {
	Status string `json:"status"`
}

type HelloResponse struct {
	Message string `json:"message"`
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
		json.NewEncoder((w)).Encode(HealthResponse{Status: "OK"})
	})

	// test api for db
	mux.HandleFunc("GET /api/db-ping", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		// when pinging, passes in context of req so is active for duration of req, stops when client exits page
		if err := pool.Ping(r.Context()); err != nil {
			w.WriteHeader(http.StatusServiceUnavailable)
			json.NewEncoder(w).Encode(HealthResponse{Status: "DB unreachable: " + err.Error()})
			return
		}
		json.NewEncoder(w).Encode(HealthResponse{Status: "OK"})
	})

	// Start server on port 8080
	log.Println("Server running on port 8080...")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(http.ListenAndServe(":8080", mux))
	}
}
