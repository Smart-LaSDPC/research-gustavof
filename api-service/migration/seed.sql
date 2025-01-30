INSERT INTO ac_sensor (temperature_current,
                       temperature_desired,
                       humidity,
                       pressure,
                       air_quality,
                       voltage,
                       current,
                       power,
                       is_on,
                       status,
                       location)
VALUES (25.1, 25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, false, 'off', 'living room'),
       (25.0, 25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, false, 'off', 'bedroom'),
       (24.9, 25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, false, 'off', 'kitchen'),
       (224.9,25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, false, 'off', 'bathroom');

SELECT * FROM ac_sensor;