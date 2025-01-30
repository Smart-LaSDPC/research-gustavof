package db

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"
	"uty-api/internal/common/constant"

	_ "github.com/jackc/pgx/v4"
	"github.com/jackc/pgx/v4/pgxpool"
)

var (
	once sync.Once
	c    ClientPool
)

type ClientPool struct {
	Conn *pgxpool.Pool
}

func NewPostgresConnectionPool(dbHost string) (*ClientPool, error) {
	var e error

	once.Do(func() {
		config, err := pgxpool.ParseConfig(dbHost)
		if err != nil {
			e = fmt.Errorf("parsing postgres config: %w", err)
			return
		}

		// Configure minimal pool settings when using PgBouncer
		config.MaxConns = 12
		config.MinConns = 3
		config.MaxConnLifetime = 1 * time.Hour
		config.MaxConnIdleTime = 15 * time.Minute
		config.HealthCheckPeriod = 1 * time.Minute

		pool, err := pgxpool.ConnectConfig(context.Background(), config)
		if err != nil {
			e = fmt.Errorf("new postgres connection pool: %w", err)
			return
		}

		c = ClientPool{Conn: pool}

		err = c.Ping()
		if err != nil {
			e = fmt.Errorf("db ping: %w", err)
			return
		}
		if e == nil {
			log.Print(constant.Green, "DB CONNECTION CREATED at: ", dbHost, constant.Reset)
		}
	})
	return &c, e
}

// Ping acquires a connection from the Pool and executes an empty sql statement against it.
// If the sql returns without error, the database Ping is considered successful, otherwise, the error is returned.
func (cp *ClientPool) Ping() error {
	c, err := cp.Conn.Acquire(context.Background())
	if err != nil {
		return fmt.Errorf("db connection is not healthy: %w", err)
	}
	defer c.Release()
	return c.Conn().Ping(context.Background())
}
