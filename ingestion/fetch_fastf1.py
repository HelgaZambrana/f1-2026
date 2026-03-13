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

def get_session(year, gp, session_type):
    session = fastf1.get_session(year, gp, session_type)
    session.load(telemetry=False, weather=False, messages=False)
    return session

def get_driver_id(abbreviation):
    result = supabase.table("drivers").select("driver_id").eq("code", abbreviation).execute()
    if result.data:
        return result.data[0]["driver_id"]
    return None

def get_or_create_session(race_name, session_type):
    race = supabase.table("races").select("race_id").eq("name", race_name).execute()
    if not race.data:
        print(f"Carrera no encontrada: {race_name}")
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

def insert_race_results(session, race_name):
    session_id = get_or_create_session(race_name, 'Race')
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

    print(f"Resultados de {race_name} insertados")


def insert_laps(session, race_name):
    session_id = get_or_create_session(race_name, 'Race')
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

    print(f"Vueltas de {race_name} insertadas")


def fetch_and_insert_pit_stops(race_name, openf1_session_key):
    url = f"https://api.openf1.org/v1/pit?session_key={openf1_session_key}"
    response = requests.get(url)
    pits = [p for p in response.json() if p["pit_duration"]]
    
    session_id = get_or_create_session(race_name, 'Race')
    if not session_id:
        return

    stop_counts = {}
    for p in pits:
        driver_number = str(p["driver_number"])
        result = supabase.table("drivers").select("driver_id").eq("driver_number", int(p["driver_number"])).execute()
        if not result.data:
            continue
        driver_id = result.data[0]["driver_id"]
        
        stop_counts[driver_id] = stop_counts.get(driver_id, 0) + 1
        
        supabase.table("pit_stops").insert({
            "session_id": session_id,
            "driver_id": driver_id,
            "lap_number": p["lap_number"],
            "stop_number": stop_counts[driver_id],
            "duration": p["pit_duration"]
        }).execute()
    
    print(f"Pit stops de {race_name} insertados")

def insert_qualifying_results(session, race_name):
    session_id = get_or_create_session(race_name, 'Q')
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

    print(f"Qualifying de {race_name} insertado")


def main():
    print("Cargando Australia 2026")
    session = get_session(2026, 'Australia', 'R')
    
    print("Insertando resultados de carrera")
    insert_race_results(session, 'Australian Grand Prix')

    print("Insertando vueltas")
    insert_laps(session, 'Australian Grand Prix')

    print("Insertando pit stops")
    fetch_and_insert_pit_stops('Australian Grand Prix', 11234)

    print("Insertando qualifying")
    session_q = get_session(2026, 'Australia', 'Q')
    insert_qualifying_results(session_q, 'Australian Grand Prix')

    print("Listo")

main()