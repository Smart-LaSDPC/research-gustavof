package air_conditioner

import (
	"context"
	"math/rand"
	"time"
)

type ACRepository interface {
	// Get all records with pagination support
	GetAll(ctx context.Context, limit, offset string) ([]AirConditionerSensorRead, error)

	// Save multiple air conditioner sensor records
	SaveMany(ctx context.Context, acColl []AirConditionerSensorWrite) (count int64, err error)

	// Create the ac_sensor table if it does not exist
	CreateTable(ctx context.Context) error
}

type AirConditionerSensorRead struct {
	ID                 int64     `json:"id"`
	TemperatureCurrent float64   `json:"temperature_current"`
	TemperatureDesired float64   `json:"temperature_desired"`
	Humidity           float64   `json:"humidity"`
	Pressure           float64   `json:"pressure"`
	AirQuality         float64   `json:"air_quality"`
	Voltage            float64   `json:"voltage"`
	Current            float64   `json:"current"`
	Power              float64   `json:"power"`
	IsOn               bool      `json:"is_on"`
	Status             string    `json:"status"`
	Location           string    `json:"location"`
	ExtractedAt        time.Time `json:"extracted_at"`
}

type AirConditionerSensorWrite struct {
	TemperatureCurrent float64 `json:"temperature_current"`
	TemperatureDesired float64 `json:"temperature_desired"`
	Humidity           float64 `json:"humidity"`
	Pressure           float64 `json:"pressure"`
	AirQuality         float64 `json:"air_quality"`
	Voltage            float64 `json:"voltage"`
	Current            float64 `json:"current"`
	Power              float64 `json:"power"`
	IsOn               bool    `json:"isOn"`
	Status             string  `json:"status"`
	Location           string  `json:"location"`
}

func createRandomAirConditionerSensor() AirConditionerSensorWrite {
	status := []string{"actuating", "ventilator", "heater", "cooling", "off"}
	location := []string{"lab 1", "lab 2", "lab 3", "lab 4", "hall", "office", "kitchen", "bathroom"}

	return AirConditionerSensorWrite{
		TemperatureCurrent: rand.Float64() * 100,
		TemperatureDesired: rand.Float64() * 100,
		Humidity:           rand.Float64() * 100,
		Pressure:           rand.Float64() * 100,
		AirQuality:         rand.Float64() * 100,
		Voltage:            rand.Float64() * 100,
		Current:            rand.Float64() * 100,
		Power:              rand.Float64() * 100,
		IsOn:               rand.Float64() > 0.5,
		Status:             status[rand.Intn(len(status))],
		Location:           location[rand.Intn(len(location))],
	}
}

func createRandomACSensorCollection(amount int) (acColl []AirConditionerSensorWrite) {
	for i := 0; i < amount; i++ {
		acColl = append(acColl, createRandomAirConditionerSensor())
	}
	return
}
