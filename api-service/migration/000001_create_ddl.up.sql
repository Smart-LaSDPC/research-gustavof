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
    extracted_at TIMESTAMP NOT NULL DEFAULT NOW()
    CONSTRAINT status_check check (status in ('actuating', 'ventilator', 'heater', 'cooling', 'off'))
);

-- Create index on extracted_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_ac_sensor_extracted_at ON ac_sensor(extracted_at);

-- Create index on id (though PostgreSQL automatically creates one for PRIMARY KEY)
CREATE INDEX IF NOT EXISTS idx_ac_sensor_id ON ac_sensor(id);