import pandas as pd
import os

# Cargar catálogos locales
drivers_df = pd.read_csv("data/processed/drivers.csv")
races_df = pd.read_csv("data/processed/races.csv")
sessions_df = pd.read_csv("data/processed/sessions.csv")

# Merge races con sessions para tener todo junto
race_sessions = sessions_df.merge(races_df, on="race_id")

def get_driver_id(code):
    result = drivers_df[drivers_df["code"] == code]["driver_id"]
    return int(result.values[0]) if len(result) > 0 else None

def get_session_id(race_name, session_type, year):
    result = race_sessions[
        (race_sessions["name"] == race_name) &
        (race_sessions["type"] == session_type) &
        (race_sessions["season"] == year)
    ]["session_id"]
    return int(result.values[0]) if len(result) > 0 else None

def transform_race(year, gp):
    gp_ref = gp.lower().replace(" ", "_")
    input_dir = f"data/processed/{year}_{gp_ref}"
    output_dir = f"data/processed/{year}_{gp_ref}/supabase"
    os.makedirs(output_dir, exist_ok=True)

    # Race results
    try:
        df = pd.read_csv(f"{input_dir}/race_results.csv")
        session_id = get_session_id(gp, 'Race', year)
        if not session_id:
            print(f"Session no encontrada: {gp} {year} Race")
        else:
            df['session_id'] = session_id
            df['driver_id'] = df['Abbreviation'].apply(get_driver_id)
            df = df.dropna(subset=['driver_id'])
            df = df.rename(columns={
                'GridPosition': 'grid_position',
                'Position': 'final_position',
                'Points': 'points',
                'Laps': 'laps_completed',
                'Status': 'status'
            })
            df['grid_position'] = df['grid_position'].fillna(0).astype(int).replace(0, pd.NA)
            df['final_position'] = df['final_position'].fillna(0).astype(int).replace(0, pd.NA)
            df['laps_completed'] = df['laps_completed'].fillna(0).astype(int).replace(0, pd.NA)
            df = df[['session_id', 'driver_id', 'grid_position', 'final_position', 'points', 'laps_completed', 'status']]
            df.to_csv(f"{output_dir}/race_results.csv", index=False)
    except Exception as e:
        print(f"Error race_results {gp} {year}: {e}")

    # Laps
    try:
        df = pd.read_csv(f"{input_dir}/laps.csv")
        session_id = get_session_id(gp, 'Race', year)
        if not session_id:
            print(f"Session no encontrada: {gp} {year} Race")
        else:
            df['session_id'] = session_id
            df['driver_id'] = df['Driver'].apply(get_driver_id)
            df = df.dropna(subset=['driver_id'])
            df = df.rename(columns={
                'LapNumber': 'lap_number',
                'LapTime': 'lap_time',
                'Sector1Time': 'sector1_time',
                'Sector2Time': 'sector2_time',
                'Sector3Time': 'sector3_time',
                'Compound': 'compound',
                'TyreLife': 'tyre_life',
                'Position': 'position',
                'IsPersonalBest': 'is_personal_best'
            })
            df['lap_number'] = df['lap_number'].fillna(0).astype(int).replace(0, pd.NA)
            df['tyre_life'] = df['tyre_life'].fillna(0).astype(int).replace(0, pd.NA)
            df['position'] = df['position'].fillna(0).astype(int).replace(0, pd.NA)
            df = df[['session_id', 'driver_id', 'lap_number', 'lap_time', 'sector1_time',
                    'sector2_time', 'sector3_time', 'compound', 'tyre_life', 'position', 'is_personal_best']]
            df.to_csv(f"{output_dir}/laps.csv", index=False)
    except Exception as e:
        print(f"Error laps {gp} {year}: {e}")

# Qualifying
    try:
        df = pd.read_csv(f"{input_dir}/qualifying.csv")
        session_id = get_session_id(gp, 'Q', year)
        if not session_id:
            print(f"Session no encontrada: {gp} {year} Q")
        else:
            df['session_id'] = session_id
            df['driver_id'] = df['Abbreviation'].apply(get_driver_id)
            df = df.dropna(subset=['driver_id'])
            df = df.rename(columns={
                'Position': 'position',
                'Q1': 'q1_time',
                'Q2': 'q2_time',
                'Q3': 'q3_time'
            })
            df['position'] = df['position'].fillna(0).astype(int).replace(0, pd.NA)
            df = df[['session_id', 'driver_id', 'position', 'q1_time', 'q2_time', 'q3_time']]
            df.to_csv(f"{output_dir}/qualifying.csv", index=False)
    except Exception as e:
        print(f"Error qualifying {gp} {year}: {e}")
        import traceback
        traceback.print_exc()

    print(f"Transformado: {gp} {year}")

CARRERAS_2025 = [
    {"year": 2025, "gp": "Australian Grand Prix"},
    {"year": 2025, "gp": "Chinese Grand Prix"},
    {"year": 2025, "gp": "Japanese Grand Prix"},
    {"year": 2025, "gp": "Bahrain Grand Prix"},
    {"year": 2025, "gp": "Saudi Arabian Grand Prix"},
    {"year": 2025, "gp": "Miami Grand Prix"},
    {"year": 2025, "gp": "Emilia Romagna Grand Prix"},
    {"year": 2025, "gp": "Monaco Grand Prix"},
    {"year": 2025, "gp": "Spanish Grand Prix"},
    {"year": 2025, "gp": "Canadian Grand Prix"},
    {"year": 2025, "gp": "Austrian Grand Prix"},
    {"year": 2025, "gp": "British Grand Prix"},
    {"year": 2025, "gp": "Belgian Grand Prix"},
    {"year": 2025, "gp": "Hungarian Grand Prix"},
    {"year": 2025, "gp": "Dutch Grand Prix"},
    {"year": 2025, "gp": "Italian Grand Prix"},
    {"year": 2025, "gp": "Azerbaijan Grand Prix"},
    {"year": 2025, "gp": "Singapore Grand Prix"},
    {"year": 2025, "gp": "United States Grand Prix"},
    {"year": 2025, "gp": "Mexico City Grand Prix"},
    {"year": 2025, "gp": "São Paulo Grand Prix"},
    {"year": 2025, "gp": "Las Vegas Grand Prix"},
    {"year": 2025, "gp": "Qatar Grand Prix"},
    {"year": 2025, "gp": "Abu Dhabi Grand Prix"},
]

def main():
    for carrera in CARRERAS_2025:
        transform_race(carrera['year'], carrera['gp'])

main()

def consolidate():
    race_results = []
    laps = []
    qualifying = []

    for carrera in CARRERAS_2025:
        gp_ref = carrera['gp'].lower().replace(" ", "_")
        base = f"data/processed/{carrera['year']}_{gp_ref}/supabase"

        try:
            race_results.append(pd.read_csv(f"{base}/race_results.csv"))
        except:
            pass
        try:
            laps.append(pd.read_csv(f"{base}/laps.csv"))
        except:
            pass
        try:
            qualifying.append(pd.read_csv(f"{base}/qualifying.csv"))
        except:
            pass

    pd.concat(race_results).to_csv("data/processed/all_race_results_2025.csv", index=False)
    pd.concat(laps).to_csv("data/processed/all_laps_2025.csv", index=False)
    pd.concat(qualifying).to_csv("data/processed/all_qualifying_2025.csv", index=False)
    print("CSVs consolidados")

consolidate()