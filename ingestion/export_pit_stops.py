import requests
import pandas as pd
import os

drivers_df = pd.read_csv("data/processed/drivers.csv")
races_df = pd.read_csv("data/processed/races.csv")
sessions_df = pd.read_csv("data/processed/sessions.csv")

race_sessions = sessions_df.merge(races_df, on="race_id")

DRIVER_NUMBER_MAP = {
    4: "NOR",
}

def get_driver_id(driver_number):
    if driver_number in DRIVER_NUMBER_MAP:
        code = DRIVER_NUMBER_MAP[driver_number]
        result = drivers_df[drivers_df["code"] == code]["driver_id"]
    else:
        result = drivers_df[drivers_df["driver_number"] == driver_number]["driver_id"]
    return int(result.values[0]) if len(result) > 0 else None

def get_session_id(race_name, year):
    result = race_sessions[
        (race_sessions["name"] == race_name) &
        (race_sessions["type"] == "Race") &
        (race_sessions["season"] == year)
    ]["session_id"]
    return int(result.values[0]) if len(result) > 0 else None

def fetch_pit_stops(race_name, year, openf1_session_key):
    url = f"https://api.openf1.org/v1/pit?session_key={openf1_session_key}"
    response = requests.get(url)
    pits = [p for p in response.json() if p["pit_duration"]]

    session_id = get_session_id(race_name, year)
    if not session_id:
        print(f"Session no encontrada: {race_name} {year}")
        return []

    rows = []
    stop_counts = {}
    seen = set()

    for p in pits:
        driver_id = get_driver_id(int(p["driver_number"]))
        if not driver_id:
            continue

        key = (session_id, driver_id, p["lap_number"])
        if key in seen:
            continue
        seen.add(key)

        stop_counts[driver_id] = stop_counts.get(driver_id, 0) + 1
        rows.append({
            "session_id": session_id,
            "driver_id": driver_id,
            "lap_number": p["lap_number"],
            "stop_number": stop_counts[driver_id],
            "duration": p["pit_duration"]
        })

    print(f"Procesado: {race_name} {year} - {len(rows)} pit stops")
    return rows

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

def main():
    all_pits = []
    for carrera in CARRERAS_2025:
        rows = fetch_pit_stops(carrera['gp'], carrera['year'], carrera['session_key'])
        all_pits.extend(rows)

    df = pd.DataFrame(all_pits)
    df.to_csv("data/processed/all_pit_stops_2025.csv", index=False)
    print(f"Total: {len(df)} pit stops exportados")

main()