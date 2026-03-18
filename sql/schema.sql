-- ============================================================
-- F1 2025-2026 - Schema
-- Base de datos: Supabase (PostgreSQL)
-- ============================================================

-- ============================================================
-- CATÁLOGOS
-- ============================================================

CREATE TABLE circuits (
    circuit_id    SERIAL PRIMARY KEY,
    circuit_ref   VARCHAR(50) UNIQUE NOT NULL,
    name          VARCHAR(100) NOT NULL,
    country       VARCHAR(50),
    city          VARCHAR(50)
);

CREATE TABLE constructors (
    constructor_id   SERIAL PRIMARY KEY,
    constructor_ref  VARCHAR(50) UNIQUE NOT NULL,
    name             VARCHAR(100) NOT NULL,
    nationality      VARCHAR(50)
);

CREATE TABLE drivers (
    driver_id        SERIAL PRIMARY KEY,
    driver_ref       VARCHAR(50) UNIQUE NOT NULL,
    code             CHAR(3),
    driver_number    SMALLINT UNIQUE,
    forename         VARCHAR(50) NOT NULL,
    surname          VARCHAR(50) NOT NULL,
    nationality      VARCHAR(50)
);

CREATE TABLE driver_seasons (
    stint_id       SERIAL PRIMARY KEY,
    driver_id      INT REFERENCES drivers(driver_id),
    constructor_id INT REFERENCES constructors(constructor_id),
    season         SMALLINT NOT NULL,
    round_start    SMALLINT,
    round_end      SMALLINT,
    UNIQUE (driver_id, season, constructor_id, round_start)
);

-- ============================================================
-- EVENTOS
-- ============================================================

CREATE TABLE races (
    race_id            SERIAL PRIMARY KEY,
    round              SMALLINT NOT NULL,
    season             SMALLINT,
    circuit_id         INT REFERENCES circuits(circuit_id),
    name               VARCHAR(100) NOT NULL,
    race_date          DATE NOT NULL,
    is_sprint_weekend  BOOLEAN DEFAULT FALSE
);

CREATE TABLE sessions (
    session_id    SERIAL PRIMARY KEY,
    race_id       INT REFERENCES races(race_id),
    type          VARCHAR(20) NOT NULL,
    session_date  TIMESTAMP
);

-- ============================================================
-- RESULTADOS
-- ============================================================

CREATE TABLE race_results (
    result_id         SERIAL PRIMARY KEY,
    session_id        INT REFERENCES sessions(session_id),
    driver_id         INT REFERENCES drivers(driver_id),
    grid_position     SMALLINT,
    final_position    SMALLINT,
    points            NUMERIC(4,1),
    laps_completed    SMALLINT,
    status            VARCHAR(50),
    fastest_lap       BOOLEAN DEFAULT FALSE,
    fastest_lap_time  INTERVAL
);

CREATE TABLE qualifying_results (
    quali_result_id  SERIAL PRIMARY KEY,
    session_id       INT REFERENCES sessions(session_id),
    driver_id        INT REFERENCES drivers(driver_id),
    position         SMALLINT,
    q1_time          INTERVAL,
    q2_time          INTERVAL,
    q3_time          INTERVAL
);

CREATE TABLE laps (
    lap_id            SERIAL PRIMARY KEY,
    session_id        INT REFERENCES sessions(session_id),
    driver_id         INT REFERENCES drivers(driver_id),
    lap_number        SMALLINT NOT NULL,
    lap_time          INTERVAL,
    sector1_time      INTERVAL,
    sector2_time      INTERVAL,
    sector3_time      INTERVAL,
    compound          VARCHAR(20),
    tyre_life         SMALLINT,
    position          SMALLINT,
    is_personal_best  BOOLEAN DEFAULT FALSE,
    track_status      VARCHAR(5),
    is_accurate       BOOLEAN DEFAULT FALSE
);

CREATE TABLE pit_stops (
    pit_stop_id   SERIAL PRIMARY KEY,
    session_id    INT REFERENCES sessions(session_id),
    driver_id     INT REFERENCES drivers(driver_id),
    lap_number    SMALLINT NOT NULL,
    stop_number   SMALLINT,
    duration      INTERVAL,
    compound_in   VARCHAR(20),
    compound_out  VARCHAR(20)
);

-- ============================================================
-- CAMPEONATO
-- ============================================================

CREATE TABLE driver_standings (
    standing_id  SERIAL PRIMARY KEY,
    race_id      INT REFERENCES races(race_id),
    driver_id    INT REFERENCES drivers(driver_id),
    position     SMALLINT,
    points       NUMERIC(5,1),
    wins         SMALLINT
);

CREATE TABLE constructor_standings (
    standing_id     SERIAL PRIMARY KEY,
    race_id         INT REFERENCES races(race_id),
    constructor_id  INT REFERENCES constructors(constructor_id),
    position        SMALLINT,
    points          NUMERIC(5,1),
    wins            SMALLINT
);

-- ============================================================
-- CONSTRAINTS
-- ============================================================

ALTER TABLE races ADD CONSTRAINT races_season_round_key UNIQUE (season, round);
ALTER TABLE race_results ADD CONSTRAINT race_results_session_driver_key UNIQUE (session_id, driver_id);
ALTER TABLE laps ADD CONSTRAINT laps_session_driver_lap_key UNIQUE (session_id, driver_id, lap_number);
ALTER TABLE qualifying_results ADD CONSTRAINT qualifying_results_session_driver_key UNIQUE (session_id, driver_id);
ALTER TABLE pit_stops ADD CONSTRAINT pit_stops_session_driver_lap_key UNIQUE (session_id, driver_id, lap_number);