import fastf1
import pandas as pd
import os

fastf1.Cache.enable_cache('cache/')

CARRERAS_2025 = [
    {"year": 2025, "gp": "Australian Grand Prix", "session_key": 9693},
    {"year": 2025, "gp": "Chinese Grand Prix", "session_key": 9998},
    {"year": 2025, "gp": "Japanese Grand Prix", "session_key": 10006},
    {"year": 2025, "gp": "Bahrain Grand Prix", "session_key": 10014},
    {"year": 2025, "gp": "Saudi Arabian Grand Prix", "session_key": 10022},
    {"year": 2025, "gp": "Miami Grand Prix", "session_key": 10033},
    {"year": 2025, "gp": "Emilia Romagna Grand Prix", "session_key": 9987},
    {"year": 2025, "gp": "Monaco Grand Prix", "session_key": 9979},
    {"year": 2025, "gp": "Spanish Grand Prix", "session_key": 9971},
    {"year": 2025, "gp": "Canadian Grand Prix", "session_key": 9963},
    {"year": 2025, "gp": "Austrian Grand Prix", "session_key": 9955},
    {"year": 2025, "gp": "British Grand Prix", "session_key": 9947},
    {"year": 2025, "gp": "Belgian Grand Prix", "session_key": 9939},
    {"year": 2025, "gp": "Hungarian Grand Prix", "session_key": 9928},
    {"year": 2025, "gp": "Dutch Grand Prix", "session_key": 9920},
    {"year": 2025, "gp": "Italian Grand Prix", "session_key": 9912},
    {"year": 2025, "gp": "Azerbaijan Grand Prix", "session_key": 9904},
    {"year": 2025, "gp": "Singapore Grand Prix", "session_key": 9896},
    {"year": 2025, "gp": "United States Grand Prix", "session_key": 9888},
    {"year": 2025, "gp": "Mexico City Grand Prix", "session_key": 9877},
    {"year": 2025, "gp": "São Paulo Grand Prix", "session_key": 9869},
    {"year": 2025, "gp": "Las Vegas Grand Prix", "session_key": 9858},
    {"year": 2025, "gp": "Qatar Grand Prix", "session_key": 9850},
    {"year": 2025, "gp": "Abu Dhabi Grand Prix", "session_key": 9839},
]

CARRERAS_2026 = [
    {"year": 2026, "gp": "Australian Grand Prix", "session_key": 11234},
]

def export_race(year, gp):
    gp_ref = gp.lower().replace(" ", "_")
    output_dir = f"data/processed/{year}_{gp_ref}"
    os.makedirs(output_dir, exist_ok=True)

    try:
        session = fastf1.get_session(year, gp, 'R')
        session.load(telemetry=False, weather=False, messages=False)

        session.results[['Abbreviation', 'GridPosition', 'Position', 'Points', 'Laps', 'Status']].to_csv(
            f"{output_dir}/race_results.csv", index=False)

        session.laps[['Driver', 'LapNumber', 'LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time',
                      'Compound', 'TyreLife', 'Position', 'IsPersonalBest']].to_csv(
            f"{output_dir}/laps.csv", index=False)

    except Exception as e:
        print(f"Error en carrera {gp} {year}: {e}")

    try:
        session_q = fastf1.get_session(year, gp, 'Q')
        session_q.load(telemetry=False, weather=False, messages=False)

        session_q.results[['Abbreviation', 'Position', 'Q1', 'Q2', 'Q3']].to_csv(
            f"{output_dir}/qualifying.csv", index=False)

    except Exception as e:
        print(f"Error en qualifying {gp} {year}: {e}")

    print(f"Exportado: {gp} {year}")

def main(desde=0, hasta=None):
    carreras = CARRERAS_2025 + CARRERAS_2026
    bloque = carreras[desde:hasta]
    for carrera in bloque:
        export_race(carrera['year'], carrera['gp'])

main(desde=0, hasta=25)