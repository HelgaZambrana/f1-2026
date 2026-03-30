-- ============================================================
-- Alpine Driver Cards 2025-2026
-- Total points per driver per season with photo URL
-- ============================================================

WITH alpine_drivers AS (
    SELECT driver_id, season, round_start, round_end, constructor_id
    FROM driver_seasons
    WHERE constructor_id = (SELECT constructor_id FROM constructors WHERE constructor_ref = 'alpine')
)

SELECT
    d.code,
    d.forename,
    d.surname,
    d.photo_url,
    ds.season,
    SUM(rr.points) AS total_points
FROM race_results rr
JOIN drivers d ON rr.driver_id = d.driver_id
JOIN sessions s ON rr.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
JOIN alpine_drivers ds ON d.driver_id = ds.driver_id
    AND ds.season = r.season
    AND r.round BETWEEN ds.round_start AND ds.round_end
WHERE s.type = 'Race'
GROUP BY d.code, d.forename, d.surname, d.photo_url, ds.season
ORDER BY ds.season, total_points DESC;