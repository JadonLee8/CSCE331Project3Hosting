package config

import (
	"errors"
	"fmt"
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	Port          string
	DBHost        string
	DBUser        string
	DBName        string
	DBPassword    string
	WeatherAPIKey string
}

func Load() (Config, error) {
	//
	if err := godotenv.Load(); err != nil && !errors.Is(err, os.ErrNotExist) {
		return Config{}, fmt.Errorf("loading .env: %w", err)
	}

	cfg := Config{
		Port:          getEnv("PORT", "8080"),
		DBHost:        getEnv("DB_HOST", "csce-315-db.engr.tamu.edu"),
		DBUser:        getEnv("DB_USER", "squad_44"),
		DBName:        getEnv("DB_NAME", "squad_44_db"),
		DBPassword:    getEnv("DB_PASSWORD", ""),
		WeatherAPIKey: getEnv("WEATHER_API", ""),
	}

	if cfg.DBPassword == "" {
		return Config{}, errors.New("DB_PASSWORD not set (add it to backend/.env)")
	}

	// nil is the Null value for Go, if err != nil means there's an error, error not equal to null
	return cfg, nil
}

// DatabaseURL builds the Postgres connection string.
func (c Config) DatabaseURL() string {
	return fmt.Sprintf("postgres://%s:%s@%s:5432/%s",
		c.DBUser, c.DBPassword, c.DBHost, c.DBName)
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
