-- ============================================================
-- Alpine Qualifying Performance 2025-2026
-- Gap to pole and head to head
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
JOIN alpine_drivers ad ON d.driver_id = ad.driver_id
    AND ad.season = r.season
    AND r.round BETWEEN ad.round_start AND ad.round_end
WHERE s.type = 'Q'
ORDER BY r.season, r.round, d.code;
