-- ============================================================
-- Alpine Tyre Degradation 2025-2026
-- Lap time evolution by compound and tyre life
-- ============================================================

WITH alpine_drivers AS (
    SELECT driver_id, season, round_start, round_end
    FROM driver_seasons
    WHERE constructor_id = (SELECT constructor_id FROM constructors WHERE constructor_ref = 'alpine')
)

SELECT
    r.season,
    r.name AS race,
    d.code AS driver,
    l.compound,
    l.tyre_life,
    AVG(EXTRACT(EPOCH FROM l.lap_time)) AS avg_lap_seconds
FROM laps l
JOIN drivers d ON l.driver_id = d.driver_id
JOIN sessions s ON l.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
JOIN alpine_drivers ad ON d.driver_id = ad.driver_id
    AND ad.season = r.season
    AND r.round BETWEEN ad.round_start AND ad.round_end
WHERE s.type = 'Race'
AND l.is_accurate = true
AND l.compound IN ('SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET')
GROUP BY r.season, r.name, d.code, l.compound, l.tyre_life
ORDER BY r.season, r.name, d.code, l.compound, l.tyre_life;