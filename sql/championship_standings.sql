-- Race performance: grid vs finish position delta
-- Positive delta = gained positions, negative = lost positions

SELECT
    r.name AS race,
    r.race_date,
    d.code AS driver,
    rr.grid_position,
    rr.final_position,
    rr.grid_position - rr.final_position AS position_delta,
    rr.points,
    rr.status
FROM race_results rr
JOIN drivers d ON rr.driver_id = d.driver_id
JOIN sessions s ON rr.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
WHERE d.code IN ('COL', 'GAS')
AND s.type = 'Race'
ORDER BY r.race_date, d.code;