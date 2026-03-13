# F1 2026 - Workflow

## Stack
- **Datos**: FastF1 + OpenF1 API
- **Base de datos**: Supabase (PostgreSQL)
- **Análisis**: SQL + Python
- **Visualización**: Tableau Public

## Estructura del proyecto
- `ingestion/fetch_openf1.py`: catálogos (pilotos, equipos, circuitos, carreras) - correr solo una vez al inicio de temporada
- `ingestion/fetch_fastf1.py`: resultados por GP (carrera, vueltas, pit stops, qualifying)
- `sql/`: queries de análisis
- `tableau/`: capturas y exports CSV para Tableau

---

## Checklist por GP

### Antes de correr el script
- [ ] Confirmar que el venv está activo: `source venv/bin/activate`
- [ ] Verificar que el GP terminó y los datos están disponibles en FastF1

### En `fetch_fastf1.py`, actualizar el `main()` con el GP nuevo
- [ ] Cambiar nombre del GP en `get_session()`
- [ ] Cambiar nombre del GP en `insert_race_results()`
- [ ] Cambiar nombre del GP en `insert_laps()`
- [ ] Cambiar `openf1_session_key` en `fetch_and_insert_pit_stops()` 
- [ ] Cambiar nombre del GP en `insert_qualifying_results()`

### Cómo obtener el session_key de OpenF1 para cada GP
Reemplazar `meeting_key` con el del GP nuevo:
https://api.openf1.org/v1/sessions?meeting_key=XXXX&session_name=Race
Los `meeting_key` están en:
https://api.openf1.org/v1/meetings?year=2026

### Correr el script
```bash
python3 ingestion/fetch_fastf1.py
```

### Después de correr el script
- [ ] Verificar filas nuevas en Supabase: `race_results`, `laps`, `pit_stops`, `qualifying_results`
- [ ] Actualizar `driver_standings` y `constructor_standings` en Supabase
- [ ] Limpiar el caché de FastF1:
```bash
rm -rf cache/*
```
- [ ] Exportar CSVs para Tableau desde Supabase
- [ ] Actualizar dashboard en Tableau Public
- [ ] Commit y push:
```bash
git add .
git commit -m "data: add [nombre GP] 2026 results"
git push origin main
```

---

## GPs sprint (is_sprint_weekend = true)
Estos GPs tienen sesión adicional. Agregar al script:
- `get_session(year, gp, 'S')` para resultados del sprint
- `get_session(year, gp, 'SQ')` para qualifying del sprint

- China (Round 2)
- Miami (Round 6)
- Canada (Round 9)
- Gran Bretaña (Round 13)
- Países Bajos (Round 17)
- Singapur (Round 19)

---

## Pendiente
- [ ] `driver_standings` y `constructor_standings` (completar cuando haya 2+ carreras)
- [ ] Queries SQL de análisis
- [ ] Dashboard Tableau