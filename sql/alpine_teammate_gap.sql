-- ============================================================
-- Alpine Teammate Qualifying Gap 2025-2026
-- Last common session methodology (Q + SQ)
-- ============================================================

WITH alpine_qualifying AS (
    SELECT
        r.season,
        r.round,
        r.name AS race,
        s.type AS session_type,
        d.code AS driver,
        EXTRACT(EPOCH FROM qr.q1_time) AS q1,
        EXTRACT(EPOCH FROM qr.q2_time) AS q2,
        EXTRACT(EPOCH FROM qr.q3_time) AS q3
    FROM qualifying_results qr
    JOIN drivers d ON qr.driver_id = d.driver_id
    JOIN sessions s ON qr.session_id = s.session_id
    JOIN races r ON s.race_id = r.race_id
    JOIN driver_seasons ds ON d.driver_id = ds.driver_id
        AND ds.season = r.season
        AND r.round BETWEEN ds.round_start AND ds.round_end
    JOIN constructors c ON ds.constructor_id = c.constructor_id
    WHERE s.type IN ('Q', 'SQ')
    AND c.constructor_ref = 'alpine'
),

paired AS (
    SELECT
        a.season,
        a.round,
        a.race,
        a.session_type,
        a.driver AS driver_a,
        b.driver AS driver_b,
        CASE
            WHEN a.q3 IS NOT NULL AND b.q3 IS NOT NULL THEN 'Q3'
            WHEN a.q2 IS NOT NULL AND b.q2 IS NOT NULL THEN 'Q2'
            ELSE 'Q1'
        END AS compared_in,
        CASE
            WHEN a.q3 IS NOT NULL AND b.q3 IS NOT NULL THEN a.q3
            WHEN a.q2 IS NOT NULL AND b.q2 IS NOT NULL THEN a.q2
            ELSE a.q1
        END AS time_a,
        CASE
            WHEN a.q3 IS NOT NULL AND b.q3 IS NOT NULL THEN b.q3
            WHEN a.q2 IS NOT NULL AND b.q2 IS NOT NULL THEN b.q2
            ELSE b.q1
        END AS time_b
    FROM alpine_qualifying a
    JOIN alpine_qualifying b
        ON a.season = b.season
        AND a.round = b.round
        AND a.session_type = b.session_type
        AND a.driver < b.driver
)

SELECT
    season,
    round,
    race,
    session_type,
    driver_a,
    driver_b,
    compared_in,
    time_a,
    time_b,
    ABS(time_a - time_b) AS gap_seconds,
    CASE WHEN time_a < time_b THEN driver_a ELSE driver_b END AS faster_driver
FROM paired
ORDER BY season, round, session_type;