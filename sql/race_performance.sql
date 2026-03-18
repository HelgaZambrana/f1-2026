-- ============================================================
-- Alpine Race Performance 2025-2026
-- Position delta: grid vs finish
-- ============================================================

WITH alpine_drivers AS (
    SELECT driver_id, season, round_start, round_end
    FROM driver_seasons
    WHERE constructor_id = (SELECT constructor_id FROM constructors WHERE constructor_ref = 'alpine')
)

SELECT
    r.season,
    r.round,
    r.name AS race,
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
JOIN alpine_drivers ad ON d.driver_id = ad.driver_id
    AND ad.season = r.season
    AND r.round BETWEEN ad.round_start AND ad.round_end
WHERE s.type = 'Race'
ORDER BY r.season, r.round, d.code;

