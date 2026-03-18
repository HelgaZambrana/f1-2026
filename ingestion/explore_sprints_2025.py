import fastf1
fastf1.Cache.enable_cache('cache/')

SPRINTS_2025 = [
    {"gp": "Chinese Grand Prix", "round": 2},
    {"gp": "Miami Grand Prix", "round": 6},
    {"gp": "Belgian Grand Prix", "round": 13},
    {"gp": "United States Grand Prix", "round": 19},
    {"gp": "São Paulo Grand Prix", "round": 21},
    {"gp": "Qatar Grand Prix", "round": 23},
]

for s in SPRINTS_2025:
    for tipo in ['SQ', 'S']:
        try:
            session = fastf1.get_session(2025, s['gp'], tipo)
            print(f"{s['gp']} {tipo} → {session}")
        except Exception as e:
            print(f"{s['gp']} {tipo} → Error: {e}")