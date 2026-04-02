import fastf1
import pandas as pd
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
fastf1.Cache.enable_cache('cache/')

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

CARRERAS = [
    {'year': 2025, 'gp': 'Australian Grand Prix'},
    {'year': 2025, 'gp': 'Chinese Grand Prix'},
    {'year': 2025, 'gp': 'Japanese Grand Prix'},
    {'year': 2025, 'gp': 'Bahrain Grand Prix'},
    {'year': 2025, 'gp': 'Saudi Arabian Grand Prix'},
    {'year': 2025, 'gp': 'Miami Grand Prix'},
    {'year': 2025, 'gp': 'Emilia Romagna Grand Prix'},
    {'year': 2025, 'gp': 'Monaco Grand Prix'},
    {'year': 2025, 'gp': 'Spanish Grand Prix'},
    {'year': 2025, 'gp': 'Canadian Grand Prix'},
    {'year': 2025, 'gp': 'Austrian Grand Prix'},
    {'year': 2025, 'gp': 'British Grand Prix'},
    {'year': 2025, 'gp': 'Belgian Grand Prix'},
    {'year': 2025, 'gp': 'Hungarian Grand Prix'},
    {'year': 2025, 'gp': 'Dutch Grand Prix'},
    {'year': 2025, 'gp': 'Italian Grand Prix'},
    {'year': 2025, 'gp': 'Azerbaijan Grand Prix'},
    {'year': 2025, 'gp': 'Singapore Grand Prix'},
    {'year': 2025, 'gp': 'United States Grand Prix'},
    {'year': 2025, 'gp': 'Mexico City Grand Prix'},
    {'year': 2025, 'gp': 'São Paulo Grand Prix'},
    {'year': 2025, 'gp': 'Las Vegas Grand Prix'},
    {'year': 2025, 'gp': 'Qatar Grand Prix'},
    {'year': 2025, 'gp': 'Abu Dhabi Grand Prix'},
    {'year': 2026, 'gp': 'Australian Grand Prix'},
    {'year': 2026, 'gp': 'Chinese Grand Prix'},
    {'year': 2026, 'gp': 'Japanese Grand Prix'},
]

for carrera in CARRERAS:
    try:
        session = fastf1.get_session(carrera['year'], carrera['gp'], 'R')
        session.load(telemetry=False, weather=True, messages=False)

        rainfall = session.weather_data['Rainfall']

        if rainfall.all():
            conditions = 'wet'
        elif rainfall.any():
            conditions = 'mixed'
        else:
            conditions = 'dry'

        supabase.table('races').update(
            {'conditions': conditions}
        ).eq('name', carrera['gp']).eq('season', carrera['year']).execute()

        print(f"{carrera['gp']} {carrera['year']}: {conditions}")

    except Exception as e:
        print(f"Error {carrera['gp']} {carrera['year']}: {e}")