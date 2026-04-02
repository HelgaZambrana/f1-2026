-- ============================================================
-- Alpine Tyre Age at Race Start 2025-2026
-- Tyre life at the beginning of each stint
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
    MIN(l.tyre_life) AS tyre_age_at_start,
    MIN(l.lap_number) AS stint_start_lap
FROM laps l
JOIN drivers d ON l.driver_id = d.driver_id
JOIN sessions s ON l.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
JOIN alpine_drivers ad ON l.driver_id = ad.driver_id
    AND ad.season = r.season
    AND r.round BETWEEN ad.round_start AND ad.round_end
WHERE s.type = 'Race'
AND l.compound IN ('SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET')
GROUP BY r.season, r.name, d.code, l.compound
ORDER BY r.season, r.name, d.code, stint_start_lap;