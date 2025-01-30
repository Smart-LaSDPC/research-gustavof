package air_conditioner

import (
	"context"
	"fmt"
	"log"
	"strings"

	"github.com/georgysavva/scany/pgxscan"
	"github.com/jackc/pgx/v4"
	"github.com/jackc/pgx/v4/pgxpool"
)

type postgres struct {
	db *pgxpool.Pool
}

func NewRepository(db *pgxpool.Pool) *postgres {
	return &postgres{
		db: db,
	}
}

// CreateTable creates the ac_sensor table if it doesn't exist
func (p postgres) CreateTable(ctx context.Context) error {
	q := `
	CREATE TABLE IF NOT EXISTS ac_sensor(
		id SERIAL NOT NULL PRIMARY KEY,
		temperature_current FLOAT NOT NULL,
		temperature_desired FLOAT NOT NULL,
		humidity FLOAT NOT NULL,
		pressure FLOAT NOT NULL,
		air_quality FLOAT NOT NULL,
		voltage FLOAT NOT NULL,
		current FLOAT NOT NULL,
		power FLOAT NOT NULL,
		is_on BOOLEAN NOT NULL,
		status VARCHAR(120) NOT NULL,
		location VARCHAR(120) NOT NULL,
		extracted_at TIMESTAMP NOT NULL DEFAULT NOW(),
		CONSTRAINT status_check CHECK (status in ('actuating', 'ventilator', 'heater', 'cooling', 'off'))
	);
	
	CREATE INDEX IF NOT EXISTS idx_ac_sensor_extracted_at ON ac_sensor(extracted_at);
	CREATE INDEX IF NOT EXISTS idx_ac_sensor_id ON ac_sensor(id);
	`

	_, err := p.db.Exec(ctx, q)
	if err != nil {
		log.Printf("[ERROR]: Could not create table ac_sensor: %v", err)
		return err
	}
	log.Println("[INFO]: Table ac_sensor created or already exists.")
	return nil
}

func (p postgres) GetAll(ctx context.Context, limit, offset string) ([]AirConditionerSensorRead, error) {
	var UserCollection []AirConditionerSensorRead
	var q strings.Builder
	q.WriteString(`
		SELECT * FROM ac_sensor
	`)

	// request with pagination - default limit is 500 if no limit is specified
	if limit == "" {
		limit = "500"
	}
	q.WriteString(fmt.Sprintf("LIMIT %s ", limit))
	if offset != "" {
		q.WriteString("OFFSET ")
		q.WriteString(offset)
	}
	err := pgxscan.Select(ctx, p.db, &UserCollection, q.String())
	if err != nil {
		log.Print("\n[ERROR]:", err)
		return nil, err
	}
	return UserCollection, nil
}

func (p postgres) SaveMany(ctx context.Context, acColl []AirConditionerSensorWrite) (id int64, err error) {
	var data [][]interface{}
	for _, ac := range acColl {
		data = append(data, []interface{}{
			ac.TemperatureCurrent,
			ac.TemperatureDesired,
			ac.Humidity,
			ac.Pressure,
			ac.AirQuality,
			ac.Voltage,
			ac.Current,
			ac.Power,
			ac.IsOn,
			ac.Status,
			ac.Location,
		})
	}
	copyCount, err := p.db.CopyFrom(
		context.Background(),
		pgx.Identifier{"ac_sensor"},
		[]string{
			"temperature_current",
			"temperature_desired",
			"humidity",
			"pressure",
			"air_quality",
			"voltage",
			"current",
			"power",
			"is_on",
			"status",
			"location",
		},
		pgx.CopyFromRows(data),
	)
	if err != nil {
		log.Println(err)
	}
	return copyCount, nil
}
