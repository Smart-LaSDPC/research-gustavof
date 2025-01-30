# Air Conditioner IoT API Service

A RESTful API service built with Go (Golang) for managing and monitoring air conditioner sensor data.

## Features

- RESTful API endpoints for air conditioner sensor data
- PostgreSQL database integration with connection pooling
- JWT-based authentication
- Docker and Docker Compose support
- Database migrations using golang-migrate
- Environment variable configuration
- Structured logging
- CORS and GZIP middleware support

## Tech Stack

- Go 1.19
- Gin Web Framework
- PostgreSQL 15
- Docker & Docker Compose
- JWT Authentication
- pgx for PostgreSQL driver
- golang-migrate for database migrations

## Prerequisites

- Go 1.19 or higher
- PostgreSQL 15
- Docker and Docker Compose (optional)


## Project Structure

api-service/
├── cmd/
│   └── main.go           # Application entry point
├── internal/
│   ├── auth/             # Authentication logic
│   ├── common/           # Shared utilities
│   ├── config/           # Configuration management
│   └── db/               # Database client
├── migration/            # Database migrations
├── pkg/
│   └── air-conditioner/  # AC sensor business logic
├── Dockerfile
├── docker-compose.yml
├── go.mod
└── go.sum


## Getting Started

1. Clone the repository

2. Set up environment variables:
   cp .env.example .env

3. Run with Docker Compose:
   docker-compose up -d

   Or run locally:
   make run


## API Endpoints

- `GET /iot` - Get all AC sensor readings
- `POST /iot/create` - Create new AC sensor readings
- `POST /iot/create_table` - Initialize AC sensor table
- Version info: `GET /version`

DEVELOPMENT
-----------
Available Make Commands:
make build      # Build the Go binary
make run        # Run the application
make dev        # Start development environment
make test       # Run tests
make network    # Create Docker network
make compose    # Start with Docker Compose
make clean      # Clean Docker resources