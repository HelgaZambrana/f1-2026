-- ============================================================
-- Alpine Gap to Pole Position 2025-2026
-- Difference between Alpine drivers and pole time per race (Q + SQ)
-- ============================================================

WITH alpine_drivers AS (
    SELECT driver_id, season, round_start, round_end
    FROM driver_seasons
    WHERE constructor_id = (SELECT constructor_id FROM constructors WHERE constructor_ref = 'alpine')
),

pole_times AS (
    SELECT
        s.session_id,
        MIN(EXTRACT(EPOCH FROM COALESCE(qr.q3_time, qr.q2_time, qr.q1_time))) AS pole_time
    FROM qualifying_results qr
    JOIN sessions s ON qr.session_id = s.session_id
    WHERE s.type IN ('Q', 'SQ')
    GROUP BY s.session_id
)

SELECT
    r.season,
    r.round,
    r.name AS race,
    s.type AS session_type,
    d.code AS driver,
    EXTRACT(EPOCH FROM COALESCE(qr.q3_time, qr.q2_time, qr.q1_time)) AS driver_time,
    pt.pole_time,
    EXTRACT(EPOCH FROM COALESCE(qr.q3_time, qr.q2_time, qr.q1_time)) - pt.pole_time AS gap_to_pole
FROM qualifying_results qr
JOIN drivers d ON qr.driver_id = d.driver_id
JOIN sessions s ON qr.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
JOIN alpine_drivers ad ON d.driver_id = ad.driver_id
    AND ad.season = r.season
    AND r.round BETWEEN ad.round_start AND ad.round_end
JOIN pole_times pt ON pt.session_id = s.session_id
WHERE s.type IN ('Q', 'SQ')
ORDER BY r.season, r.round, s.type, d.code;