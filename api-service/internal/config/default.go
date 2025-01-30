package config

import (
	"fmt"
	"os"
	"strconv"
)

const (
	defaultPostgresURL = "postgres://domino-de:domino-de@postgres:5432/domino-de?sslmode=disable"
)

// GetEnvString returns the value as a string of the environment
// variable that matches the key, if not found it returns the default value.
func GetEnvString(key, defaultValue string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}

	return defaultValue
}

// GetEnvBool returns the value as boolean of the environment
// variable that matches the key, if not found it returns the default value.
func GetEnvBool(key string, defaultValue bool) bool {
	if val := os.Getenv(key); val != "" {
		bVal, err := strconv.ParseBool(val)
		if err != nil {
			return defaultValue
		}
		return bVal
	}

	return defaultValue
}

// GetEnvInt returns the value as integer of the environment
// variable that matches the key, if not found it returns the default value.
func GetEnvInt(key string, def int) int {
	val, err := strconv.Atoi(GetEnvString(key, fmt.Sprintf("%d", def)))
	if err != nil {
		return def
	}

	return val
}
