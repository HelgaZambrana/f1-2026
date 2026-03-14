import requests
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def fetch_drivers():
    url = "https://api.openf1.org/v1/drivers?session_key=latest"
    response = requests.get(url)
    drivers = response.json()
    return drivers


def insert_constructors(drivers):
    equipos = list(set([d["team_name"] for d in drivers if d["team_name"]]))
    
    for equipo in equipos:
        constructor_ref = equipo.lower().replace(" ", "_")
        supabase.table("constructors").upsert({
            "constructor_ref": constructor_ref,
            "name": equipo,
        }, on_conflict="constructor_ref").execute()
    
    print(f"{len(equipos)} constructores insertados")


def insert_drivers(drivers):
    for d in drivers:
        if not d["team_name"]:
            continue
            
        constructor_ref = d["team_name"].lower().replace(" ", "_")
        constructor = supabase.table("constructors").select("constructor_id").eq("constructor_ref", constructor_ref).execute()
        constructor_id = constructor.data[0]["constructor_id"]
        
        supabase.table("drivers").upsert({
            "driver_ref": d["name_acronym"].lower(),
            "code": d["name_acronym"],
            "forename": d["first_name"],
            "surname": d["last_name"],
            "nationality": d.get("country_code"),
            "constructor_id": constructor_id
        }, on_conflict="driver_ref").execute()
    
    print(f"{len(drivers)} pilotos procesados")


def fetch_races(year):
    url = f"https://api.openf1.org/v1/meetings?year={year}"
    response = requests.get(url)
    meetings = response.json()
    gps = [m for m in meetings if "Grand Prix" in m["meeting_name"]]
    print(f"{len(gps)} GPs encontrados para {year}")
    return gps


def insert_circuits(races):
    for r in races:
        circuit_ref = r["circuit_short_name"].lower().replace(" ", "_")
        supabase.table("circuits").upsert({
            "circuit_ref": circuit_ref,
            "name": r["circuit_short_name"],
            "country": r["country_name"],
            "city": r["location"]
        }, on_conflict="circuit_ref").execute()
    
    print(f"{len(races)} circuitos insertados")


def insert_races(races, season):
    for r in races:
        circuit_ref = r["circuit_short_name"].lower().replace(" ", "_")
        circuit = supabase.table("circuits").select("circuit_id").eq("circuit_ref", circuit_ref).execute()
        circuit_id = circuit.data[0]["circuit_id"]
        
        supabase.table("races").upsert({
            "round": races.index(r) + 1,
            "season": season,
            "circuit_id": circuit_id,
            "name": r["meeting_name"],
            "race_date": r["date_start"][:10],
            "is_sprint_weekend": False
        }, on_conflict="season,round").execute()
    
    print(f"{len(races)} carreras insertadas para {season}")

def main():
    print("Procesando drivers")
    drivers = fetch_drivers()
    insert_constructors(drivers)
    insert_drivers(drivers)

    for year in [2025, 2026]:
        print(f"Procesando GPs {year}")
        races = fetch_races(year)
        insert_circuits(races)
        insert_races(races, year)

    print("Listo")

main()