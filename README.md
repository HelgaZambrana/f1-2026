# F1 2026 Season Tracker — Alpine Focus

Real-time data pipeline and analysis of the 2026 Formula 1 season,
with a focus on the Alpine F1 Team and their current drivers Pierre Gasly and Franco Colapinto.

Built as a portfolio project combining data engineering and analytics
across a full racing season.

---

## Motivation

The 2026 season marks one of the biggest regulation overhauls in F1 history,
making it a unique moment to track team and driver performance as the field
adapts to new cars, power units and racing dynamics.

---

## Stack

| Tool | Purpose |
|---|---|
| Python | Data ingestion and processing |
| FastF1 | Race data: lap times, results, pit stops |
| OpenF1 API | Catalogue data: drivers, constructors, circuits |
| PostgreSQL (Supabase) | Cloud database |
| SQL | Analysis and data transformation |
| Tableau Public | Dashboard and visualization |

---

## Data Sources

**FastF1** is a Python library that connects to official F1 timing servers.
It provides lap-by-lap data including sector times, tyre compounds and race results.
Data becomes available shortly after each session ends.

**OpenF1** is a free REST API providing structured F1 data including
driver and constructor catalogues, pit stop durations and session metadata.

---

## Project Structure
```
f1-2026/
├── data/
│   ├── raw/          # raw data from APIs (not tracked by git)
│   └── processed/    # clean CSVs ready for Tableau
├── ingestion/
│   ├── fetch_openf1.py   # loads catalogues (run once per season)
│   └── fetch_fastf1.py   # loads race results (run after each GP)
├── sql/              # analysis queries
├── tableau/          # dashboard exports and screenshots
├── WORKFLOW.md       # step-by-step checklist for each GP
└── requirements.txt
```

---

## Key Questions

This project aims to answer the following analytical questions across the season:

1. **Points and positions** — Which races did Alpine score points in and what was the grid vs finish position delta?
2. **Tyre degradation** — How does lap time evolve as tyre life increases across different compounds?
3. **Qualifying performance** — How do Gasly and Colapinto compare in qualifying, sector by sector?
4. **Pit stop strategy** — How does Alpine's pit stop duration and strategy compare to midfield rivals?