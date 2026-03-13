import fastf1
import pandas as pd
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


def main():
    print("Cargando Australia 2026")
    session = get_session(2026, 'Australia', 'R')
    
    print("Insertando resultados de carrera")
    insert_race_results(session, 'Australian Grand Prix')
    
    print("Listo")

main()