-- ============================================================
-- Alpine Pit Stop Position Change 2025-2026
-- Position before and after each pit stop
-- ============================================================

WITH alpine_drivers AS (
    SELECT driver_id, season, round_start, round_end
    FROM driver_seasons
    WHERE constructor_id = (SELECT constructor_id FROM constructors WHERE constructor_ref = 'alpine')
),

pit_laps AS (
    SELECT
        ps.session_id,
        ps.driver_id,
        ps.lap_number AS pit_lap,
        ps.stop_number
    FROM pit_stops ps
),

position_before AS (
    SELECT
        l.session_id,
        l.driver_id,
        l.lap_number,
        l.position AS pos_before
    FROM laps l
),

position_after AS (
    SELECT
        l.session_id,
        l.driver_id,
        l.lap_number,
        l.position AS pos_after
    FROM laps l
)

SELECT
    r.season,
    r.round,
    r.name AS race,
    r.conditions,
    d.code AS driver,
    pl.stop_number,
    pl.pit_lap,
    pb.pos_before,
    pa.pos_after,
    pb.pos_before - pa.pos_after AS position_gain
FROM pit_laps pl
JOIN drivers d ON pl.driver_id = d.driver_id
JOIN sessions s ON pl.session_id = s.session_id
JOIN races r ON s.race_id = r.race_id
JOIN alpine_drivers ad ON d.driver_id = ad.driver_id
    AND ad.season = r.season
    AND r.round BETWEEN ad.round_start AND ad.round_end
JOIN position_before pb ON pb.session_id = pl.session_id
    AND pb.driver_id = pl.driver_id
    AND pb.lap_number = pl.pit_lap
JOIN position_after pa ON pa.session_id = pl.session_id
    AND pa.driver_id = pl.driver_id
    AND pa.lap_number = pl.pit_lap + 1
WHERE s.type = 'Race'
ORDER BY r.season, r.round, d.code, pl.stop_number;