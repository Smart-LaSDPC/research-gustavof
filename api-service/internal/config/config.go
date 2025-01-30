package config

import (
	"errors"
	"fmt"
	"log"
	"os"
	"strings"
	"uty-api/internal/common/constant"

	"github.com/joho/godotenv"
	_ "github.com/joho/godotenv"
	_ "github.com/joho/godotenv/autoload"
)

// Config is the central configuration structure that holds all application settings
// sourced from environment variables.
type Config struct {
	// Environment specifies the running environment (e.g., "development", "production")
	Environment string `json:"environment,omitempty"`
	// GinPort specifies the port on which the Gin server will listen
	GinPort string `json:"gin_port,omitempty"`
	// PostgresURL is the connection URL for PostgreSQL
	PostgresURL string `json:"postgres_url"`
	// PostgresDSN is the connection string for PostgreSQL
	PostgresDSN string `json:"postgres_dsn,omitempty"`
	// RedisAddress is the connection address for Redis
	RedisAddress string `json:"redis_address"`
	// RedisPassword is the authentication password for Redis
	RedisPassword string `json:"redis_password"`
	// Gin mode
	Debug bool `json:"debug"`
}

// Validate performs validation checks on the configuration
func (c *Config) Validate() error {
	if c.Environment == "" {
		return errors.New("environment must not be empty")
	}
	if c.PostgresURL == "" && c.PostgresDSN == "" {
		return errors.New("either PostgresURL or PostgresDSN must be provided")
	}
	if c.RedisAddress == "" {
		return errors.New("redis address must not be provided")
	}
	return nil
}

// getSQLMode converts a boolean SSL setting to the appropriate Postgres sslmode
func getSQLMode(sslEnabled string) string {
	// Convert string to lowercase for case-insensitive comparison
	sslLower := strings.ToLower(sslEnabled)
	if sslLower == "true" || sslLower == "1" || sslLower == "yes" || sslLower == "require" {
		return "require"
	}
	return "disable"
}

// GetConfig returns default config with validation.
func GetConfig() (*Config, error) {
	// Try multiple possible env file locations
	envPaths := []string{
		".env",    // Current directory
		"../.env", // Parent directory
	}

	envLoaded := false
	for _, envPath := range envPaths {
		if err := godotenv.Load(envPath); err == nil {
			envLoaded = true
			break
		}
	}

	if !envLoaded {
		log.Printf("Warning: .env file not found, using environment variables")
	}

	// Set default environment if not provided
	env := os.Getenv("ENVIRONMENT")
	if env == "" {
		env = "QA"
		os.Setenv("ENVIRONMENT", env)
	}
	log.Printf("%sENVIRONMENT: %s  %s", constant.Green, env, constant.Reset)

	// POSTGRES
	var postgresDSN, postgresURL string

	// Validate required Postgres environment variables
	requiredPostgresVars := []string{
		"POSTGRES_USER",
		"POSTGRES_PASSWORD",
		"POSTGRES_HOST",
		"POSTGRES_DATABASE",
	}

	missingVars := validateRequiredEnvVars(requiredPostgresVars)
	if len(missingVars) > 0 {
		if defaultPostgresURL == "" {
			return nil, fmt.Errorf("missing required Postgres environment variables: %v and no default URL provided", missingVars)
		}
		postgresURL = defaultPostgresURL
	} else {
		// Update SSL mode handling
		sslMode := getSQLMode(GetEnvString("POSTGRES_SSL", "false"))
		postgresPort := GetEnvString("POSTGRES_PORT", "5432")

		// Validate port number
		if !isValidPort(postgresPort) {
			return nil, fmt.Errorf("invalid postgres port: %s", postgresPort)
		}

		postgresDSN = fmt.Sprintf(
			"host=%v user=%v password=%v dbname=%v port=%v sslmode=%v",
			os.Getenv("POSTGRES_HOST"),
			os.Getenv("POSTGRES_USER"),
			os.Getenv("POSTGRES_PASSWORD"),
			os.Getenv("POSTGRES_DATABASE"),
			postgresPort,
			sslMode,
		)
		postgresURL = fmt.Sprintf(
			"postgres://%v:%v@%v:%v/%v?sslmode=%v",
			os.Getenv("POSTGRES_USER"),
			os.Getenv("POSTGRES_PASSWORD"),
			os.Getenv("POSTGRES_HOST"),
			postgresPort,
			os.Getenv("POSTGRES_DATABASE"),
			sslMode,
		)
	}

	config := &Config{
		Environment:   env,
		GinPort:       GetEnvString("GIN_PORT", "8080"),
		PostgresURL:   postgresURL,
		PostgresDSN:   postgresDSN,
		RedisAddress:  GetEnvString("REDIS_ADDRESS", "localhost:6379"),
		RedisPassword: GetEnvString("REDIS_PASSWORD", ""),
	}

	// Validate the configuration
	if err := config.Validate(); err != nil {
		return nil, fmt.Errorf("invalid configuration: %w", err)
	}

	return config, nil
}

// Helper functions

// validateRequiredEnvVars checks if all required environment variables are set
func validateRequiredEnvVars(vars []string) []string {
	var missingVars []string
	for _, v := range vars {
		if os.Getenv(v) == "" {
			missingVars = append(missingVars, v)
		}
	}
	return missingVars
}

// isValidPort checks if the port string is valid
func isValidPort(port string) bool {
	// Add port validation logic here
	// For example, check if it's a number between 1 and 65535
	return true // Placeholder
}
