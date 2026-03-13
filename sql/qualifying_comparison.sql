-- Qualifying comparison: Colapinto vs Gasly
-- Gap to pole and head to head by session

SELECT
    r.name AS race,
    d.code AS driver,
    qr.position,
    EXTRACT(EPOCH FROM qr.q1_time) AS q1_seconds,
    EXTRACT(EPOCH FROM qr.q2_time) AS q2_seconds,
    EXTRACT(EPOCH FROM qr.q3_time) AS q3_seconds,
    EXTRACT(EPOCH FROM qr.q1_time) - MIN(EXTRACT(EPOCH FROM qr.q1_time)) 
        OVER (PARTITION BY s.session_id) AS q1_gap_to_best,
    EXTRACT(EPOCH FROM qr.q2_time) - MIN(EXTRACT(EPOCH FROM qr.q2_time)) 
        OVER (PARTITION BY s.session_id) AS q2_gap_to_best
FROM qualifying_results qr
JOIN drivers d ON qr.driver_id = d.driver_id
JOIN sessions s ON qr.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
WHERE d.code IN ('COL', 'GAS')
ORDER BY r.race_date, d.code;