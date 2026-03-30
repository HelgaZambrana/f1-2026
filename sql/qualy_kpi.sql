-- ============================================================
-- Alpine Qualifying KPI by Driver and Season
-- Best and average qualifying position
-- ============================================================

WITH alpine_drivers AS (
    SELECT driver_id, season, round_start, round_end
    FROM driver_seasons
    WHERE constructor_id = (SELECT constructor_id FROM constructors WHERE constructor_ref = 'alpine')
)

SELECT
    d.code,
    d.forename,
    d.surname,
    d.photo_url,
    ds.season,
    MIN(qr.position) AS best_qualifying,
    ROUND(AVG(qr.position), 1) AS avg_qualifying
FROM qualifying_results qr
JOIN drivers d ON qr.driver_id = d.driver_id
JOIN sessions s ON qr.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
JOIN alpine_drivers ds ON d.driver_id = ds.driver_id
    AND ds.season = r.season
    AND r.round BETWEEN ds.round_start AND ds.round_end
WHERE s.type = 'Q'
GROUP BY d.code, d.forename, d.surname, d.photo_url, ds.season
ORDER BY ds.season, d.code;