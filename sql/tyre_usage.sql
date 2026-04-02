-- ============================================================
-- Alpine Tyre Usage 2025-2026
-- Percentage of stints per compound per race
-- ============================================================

WITH alpine_drivers AS (
    SELECT driver_id, season, round_start, round_end
    FROM driver_seasons
    WHERE constructor_id = (SELECT constructor_id FROM constructors WHERE constructor_ref = 'alpine')
),

stints AS (
    SELECT
        r.season,
        r.name AS race,
        r.race_id,
        l.driver_id,
        l.compound,
        MIN(l.tyre_life) AS stint_start
    FROM laps l
    JOIN sessions s ON l.session_id = s.session_id
    JOIN races r ON s.race_id = r.race_id
    JOIN alpine_drivers ad ON l.driver_id = ad.driver_id
        AND ad.season = r.season
        AND r.round BETWEEN ad.round_start AND ad.round_end
    WHERE s.type = 'Race'
    AND l.compound IN ('SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET')
    AND l.is_accurate = true
    GROUP BY r.season, r.name, r.race_id, l.driver_id, l.compound
),

tyre_images AS (
    SELECT 'SOFT'         AS compound, 'https://tyre-assets.pirelli.com/staticfolder/Tyre/resources/img/red-parentesi.png'    AS image_url UNION ALL
    SELECT 'MEDIUM',                   'https://tyre-assets.pirelli.com/staticfolder/Tyre/resources/img/yellow-parentesi.png' UNION ALL
    SELECT 'HARD',                     'https://tyre-assets.pirelli.com/staticfolder/Tyre/resources/img/white-parentesi.png'  UNION ALL
    SELECT 'INTERMEDIATE',             'https://upload.wikimedia.org/wikipedia/commons/a/a3/F1_tire_Pirelli_PZero_Green_2019.png' UNION ALL
    SELECT 'WET',                      'https://tyre-assets.pirelli.com/staticfolder/Tyre/resources/img/blue-parentesi.png'
)

SELECT
    s.season,
    s.race,
    r.conditions,
    s.compound,
    COUNT(*) AS total_stints,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY s.race_id) AS pct_stints,
    ti.image_url
FROM stints s
JOIN races r ON s.race = r.name AND s.season = r.season
JOIN tyre_images ti ON s.compound = ti.compound
GROUP BY s.season, s.race, s.race_id, r.conditions, s.compound, ti.image_url
ORDER BY s.season, s.race, s.compound;