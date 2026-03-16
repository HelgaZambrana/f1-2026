import fastf1
import pandas as pd
import requests
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

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

def get_session(year, gp, session_type):
    session = fastf1.get_session(year, gp, session_type)
    session.load(telemetry=False, weather=False, messages=False)
    return session

def get_driver_id(abbreviation):
    result = supabase.table("drivers").select("driver_id").eq("code", abbreviation).execute()
    if result.data:
        return result.data[0]["driver_id"]
    return None

def get_or_create_session(race_name, session_type, year):
    race = supabase.table("races").select("race_id").eq("name", race_name).eq("season", year).execute()
    if not race.data:
        print(f"Carrera no encontrada: {race_name} {year}")
        return None
    race_id = race.data[0]["race_id"]

    session = supabase.table("sessions").select("session_id").eq("race_id", race_id).eq("type", session_type).execute()
    if session.data:
        return session.data[0]["session_id"]

    new_session = supabase.table("sessions").insert({
        "race_id": race_id,
        "type": session_type
    }).execute()
    return new_session.data[0]["session_id"]

def insert_race_results(session, race_name, year):
    session_id = get_or_create_session(race_name, 'Race', year)
    if not session_id:
        return

    for _, row in session.results.iterrows():
        driver_id = get_driver_id(row['Abbreviation'])
        if not driver_id:
            continue

        supabase.table("race_results").upsert({
            "session_id": session_id,
            "driver_id": driver_id,
            "grid_position": int(row['GridPosition']) if pd.notna(row['GridPosition']) else None,
            "final_position": int(row['Position']) if pd.notna(row['Position']) else None,
            "points": float(row['Points']) if pd.notna(row['Points']) else None,
            "laps_completed": int(row['Laps']) if pd.notna(row['Laps']) else None,
            "status": row['Status']
        }, on_conflict="session_id,driver_id").execute()

    print(f"Resultados de {race_name} {year} insertados")

def insert_laps(session, race_name, year):
    session_id = get_or_create_session(race_name, 'Race', year)
    if not session_id:
        return

    for _, lap in session.laps.iterrows():
        driver_id = get_driver_id(lap['Driver'])
        if not driver_id:
            continue

        supabase.table("laps").upsert({
            "session_id": session_id,
            "driver_id": driver_id,
            "lap_number": int(lap['LapNumber']) if pd.notna(lap['LapNumber']) else None,
            "lap_time": str(lap['LapTime']) if pd.notna(lap['LapTime']) else None,
            "sector1_time": str(lap['Sector1Time']) if pd.notna(lap['Sector1Time']) else None,
            "sector2_time": str(lap['Sector2Time']) if pd.notna(lap['Sector2Time']) else None,
            "sector3_time": str(lap['Sector3Time']) if pd.notna(lap['Sector3Time']) else None,
            "compound": lap['Compound'] if pd.notna(lap['Compound']) else None,
            "tyre_life": int(lap['TyreLife']) if pd.notna(lap['TyreLife']) else None,
            "position": int(lap['Position']) if pd.notna(lap['Position']) else None,
            "is_personal_best": bool(lap['IsPersonalBest'])
        }, on_conflict="session_id,driver_id,lap_number").execute()

    print(f"Vueltas de {race_name} {year} insertadas")

def fetch_and_insert_pit_stops(race_name, openf1_session_key, year):
    url = f"https://api.openf1.org/v1/pit?session_key={openf1_session_key}"
    response = requests.get(url)
    pits = [p for p in response.json() if p["pit_duration"]]

    session_id = get_or_create_session(race_name, 'Race', year)
    if not session_id:
        return

    stop_counts = {}
    for p in pits:
        result = supabase.table("drivers").select("driver_id").eq("driver_number", int(p["driver_number"])).execute()
        if not result.data:
            continue
        driver_id = result.data[0]["driver_id"]

        stop_counts[driver_id] = stop_counts.get(driver_id, 0) + 1

        supabase.table("pit_stops").upsert({
            "session_id": session_id,
            "driver_id": driver_id,
            "lap_number": p["lap_number"],
            "stop_number": stop_counts[driver_id],
            "duration": p["pit_duration"]
        }, on_conflict="session_id,driver_id,lap_number").execute()

    print(f"Pit stops de {race_name} {year} insertados")

def insert_qualifying_results(session, race_name, year):
    session_id = get_or_create_session(race_name, 'Q', year)
    if not session_id:
        return

    for _, row in session.results.iterrows():
        driver_id = get_driver_id(row['Abbreviation'])
        if not driver_id:
            continue

        supabase.table("qualifying_results").upsert({
            "session_id": session_id,
            "driver_id": driver_id,
            "position": int(row['Position']) if pd.notna(row['Position']) else None,
            "q1_time": str(row['Q1']) if pd.notna(row['Q1']) else None,
            "q2_time": str(row['Q2']) if pd.notna(row['Q2']) else None,
            "q3_time": str(row['Q3']) if pd.notna(row['Q3']) else None,
        }, on_conflict="session_id,driver_id").execute()

    print(f"Qualifying de {race_name} {year} insertado")

def main():
    for carrera in CARRERAS_2025 + CARRERAS_2026:
        print(f"\nProcesando {carrera['gp']} {carrera['year']}")

        session = get_session(carrera['year'], carrera['gp'], 'R')
        insert_race_results(session, carrera['gp'], carrera['year'])
        insert_laps(session, carrera['gp'], carrera['year'])
        fetch_and_insert_pit_stops(carrera['gp'], carrera['session_key'], carrera['year'])

        session_q = get_session(carrera['year'], carrera['gp'], 'Q')
        insert_qualifying_results(session_q, carrera['gp'], carrera['year'])

main()