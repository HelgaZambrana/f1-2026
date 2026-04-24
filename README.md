# F1 2025-2026 Season Tracker — Alpine Focus

Data pipeline and analysis of the 2025 and 2026 Formula 1 seasons,
with a focus on the Alpine F1 Team and their drivers Pierre Gasly,
Franco Colapinto and Jack Doohan.

Built as a portfolio project combining data engineering and analytics
across a full racing season.

---

## Motivation

Alpine is one of the most interesting teams to track analytically:
a mid-season driver change in 2025 (Doohan → Colapinto at round 7),
a car that struggled all season and a significant regulation overhaul in 2026
that changed the competitive order. This project tracks how the team evolved
across both seasons using real race data.

---

## Architecture
FastF1 + OpenF1 API
↓
Python ingestion pipeline (automated via GitHub Actions)
↓
PostgreSQL · Supabase (12 relational tables)
↓
SQL analysis (CTEs, window functions)
↓
Tableau Public (5 interactive dashboards)

The pipeline runs automatically every Sunday after each race.
New data is inserted incrementally without touching historical records.

---

## Stack

| Tool | Purpose |
|---|---|
| Python | Data ingestion and processing |
| FastF1 | Race data: lap times, results, tyre compounds, weather |
| OpenF1 API | Catalogue data: drivers, constructors, pit stops |
| PostgreSQL (Supabase) | Cloud database with 12 relational tables |
| SQL | Analysis queries with CTEs and window functions |
| Tableau Public | Interactive dashboards |
| GitHub Actions | Automated weekly pipeline execution |

---

## Data Sources

**FastF1** is a Python library that connects to official F1 timing servers.
It provides lap-by-lap data including sector times, tyre compounds, race results
and the `is_accurate` flag used to filter out safety car and anomalous laps.
Data becomes available shortly after each session ends.

**OpenF1** is a free REST API providing structured F1 data including
driver and constructor catalogues, pit stop durations and session metadata.

---

## Project Structure
f1-2026/
├── .github/
│   └── workflows/
│       └── fetch_race_data.yml  # automated Sunday pipeline
├── data/
│   ├── raw/          # raw data from APIs (not tracked by git)
│   └── processed/    # clean CSVs ready for Tableau (not tracked by git)
├── ingestion/
│   ├── fetch_openf1.py           # loads catalogues (run once per season)
│   ├── fetch_fastf1.py           # loads race results (automated)
│   ├── fetch_conditions.py       # loads weather conditions per race
│   ├── export_to_csv.py          # historical bulk export from FastF1
│   ├── export_pit_stops.py       # historical pit stops from OpenF1
│   └── transform_for_supabase.py # transforms historical CSVs for Supabase import
├── sql/
│   ├── schema.sql                    # database schema
│   ├── race_performance.sql          # race + sprint results
│   ├── qualifying_comparison.sql     # qualifying + SQ times
│   ├── alpine_driver_cards.sql       # points per driver
│   ├── alpine_teammate_gap.sql       # teammate qualifying gap
│   ├── gap_to_pole.sql               # gap to pole position
│   ├── qualy_kpi.sql                 # best and avg qualifying position
│   ├── tyre_analysis.sql             # lap time vs tyre life
│   ├── tyre_usage.sql                # tyre strategy per race
│   └── tyre_age_at_start.sql         # tyre age at stint start
├── tableau/          # dashboard exports and screenshots
├── WORKFLOW.md       # step-by-step checklist for each GP
├── ANALYSIS.md       # analytical findings and insights
└── requirements.txt

---

## Dashboards

Published on Tableau Public: https://public.tableau.com/app/profile/helga.zambrana/viz/F1_Alpine/Race

- **Race Overview** — Final positions, points, status distribution and position delta per race
- **Sprint Overview** — Same metrics for sprint races
- **Qualifying Overview** — Grid positions, teammate gap and gap to pole
- **Sprint Qualifying Overview** — Same metrics for sprint qualifying
- **Tyre Strategy** — Tyre usage, degradation, pit stop effectiveness and midfield comparison

---

## Key Findings (2025)

- Gasly was the fastest Alpine driver in qualifying in 19 of 26 races
- Average teammate qualifying gap was 0.4s, with Las Vegas as the biggest outlier (1.9s)
- Colapinto outqualified Gasly in Canada, Hungary, Italy, Azerbaijan and Singapore
- Alpine consistently loses positions at pit stops, reflecting car pace rather than strategy
- Analysis of 2026 is ongoing and updated after each GP

---

## Data Engineering Notes

The dashboard appears simple but relies on a relational database behind the scenes.
Adding a new GP takes minutes: the Python pipeline inserts only new data without
touching the historical records. Complex calculations like teammate gap
(last common session methodology) and tyre degradation filtering
(`is_accurate = true`) are resolved in SQL before reaching Tableau.

The ingestion pipeline runs automatically via GitHub Actions every Sunday after
each race. Race dates are defined in the script and the correct GP is detected
automatically based on the current date.