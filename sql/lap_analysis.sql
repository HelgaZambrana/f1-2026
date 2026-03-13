-- Tyre degradation per stint
-- Shows how lap time evolves as tyre life increases


SELECT
    d.code,
    l.compound,
    l.tyre_life,
    AVG(EXTRACT(EPOCH FROM l.lap_time)) AS avg_lap_seconds
FROM laps l
JOIN drivers d ON l.driver_id = d.driver_id
JOIN sessions s ON l.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
WHERE d.code IN ('COL', 'GAS')
AND s.type = 'Race'
AND l.lap_time IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM pit_stops ps
    WHERE ps.session_id = l.session_id
    AND ps.driver_id = l.driver_id
    AND ps.lap_number = l.lap_number
)
GROUP BY d.code, l.compound, l.tyre_life
ORDER BY d.code, l.compound, l.tyre_life;