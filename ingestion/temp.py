import fastf1
fastf1.Cache.enable_cache('cache/')

session = fastf1.get_session(2026, 'Australia', 'R')
session.load(telemetry=False, weather=False, messages=False)
print(session.laps.columns.tolist())