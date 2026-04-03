-- ============================================================
-- Midfield Tyre Strategy Comparison 2025-2026
-- Alpine vs direct rivals: stint length, stops and compounds
-- ============================================================

WITH midfield_drivers AS (
    SELECT 
        ds.driver_id, 
        ds.season, 
        ds.round_start, 
        ds.round_end,
        c.name AS constructor,
        c.constructor_ref
    FROM driver_seasons ds
    JOIN constructors c ON ds.constructor_id = c.constructor_id
    WHERE c.constructor_ref IN ('alpine', 'haas_f1_team', 'kick_sauber', 'audi', 'racing_bulls', 'williams')
),

stints AS (
    SELECT
        r.season,
        r.round,
        r.name AS race,
        md.constructor,
        d.code AS driver,
        l.compound,
        MIN(l.tyre_life) AS tyre_age_at_start,
        MIN(l.lap_number) AS stint_start_lap,
        MAX(l.lap_number) AS stint_end_lap,
        MAX(l.lap_number) - MIN(l.lap_number) + 1 AS stint_length
    FROM laps l
    JOIN drivers d ON l.driver_id = d.driver_id
    JOIN sessions s ON l.session_id = s.session_id
    JOIN races r ON s.race_id = r.race_id
    JOIN midfield_drivers md ON l.driver_id = md.driver_id
        AND md.season = r.season
        AND r.round BETWEEN md.round_start AND md.round_end
    WHERE s.type = 'Race'
    AND l.compound IN ('SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET')
    AND l.is_accurate = true
    GROUP BY r.season, r.round, r.name, md.constructor, d.code, l.compound
),

stop_counts AS (
    SELECT
        season,
        round,
        race,
        constructor,
        driver,
        COUNT(*) AS total_stints,
        COUNT(*) - 1 AS total_stops,
        AVG(stint_length) AS avg_stint_length
    FROM stints
    GROUP BY season, round, race, constructor, driver
)

SELECT
    s.season,
    s.round,
    s.race,
    s.constructor,
    s.driver,
    s.compound,
    s.tyre_age_at_start,
    s.stint_start_lap,
    s.stint_end_lap,
    s.stint_length,
    sc.total_stops,
    sc.avg_stint_length
FROM stints s
JOIN stop_counts sc ON s.season = sc.season
    AND s.round = sc.round
    AND s.driver = sc.driver
ORDER BY s.season, s.round, s.constructor, s.driver, s.stint_start_lap;