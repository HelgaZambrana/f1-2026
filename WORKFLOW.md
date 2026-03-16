# F1 2025-2026 - Workflow

## Stack
- **Datos**: FastF1 + OpenF1 API
- **Base de datos**: Supabase (PostgreSQL)
- **Análisis**: SQL + Python
- **Visualización**: Tableau Public

## Estructura del proyecto
- `ingestion/fetch_openf1.py` → catálogos (pilotos, equipos, circuitos, carreras) - correr una vez por temporada
- `ingestion/fetch_fastf1.py` → resultados por GP en curso (2026)
- `ingestion/export_to_csv.py` → exporta datos históricos de FastF1 a CSV
- `ingestion/transform_for_supabase.py` → transforma CSVs históricos para importar a Supabase
- `ingestion/export_pit_stops.py` → exporta pit stops históricos desde OpenF1
- `sql/` → queries de análisis
- `tableau/` → capturas y exports CSV para Tableau

---

## Reglas antes de arrancar cualquier ingesta

1. Explorar la fuente de datos primero - verificar qué devuelve la API antes de diseñar cualquier estructura
2. Verificar tipos de datos, nulls y duplicados en los datos crudos
3. Testear con una sola sesión o carrera
4. Validar el resultado en Supabase antes de escalar
5. Los errores nunca deben silenciarse, siempre loggear qué falló y por qué

---

## Checklist por GP (2026 en curso)

### Antes de correr el script
- [ ] Confirmar que el venv está activo: `source venv/bin/activate`
- [ ] Verificar que el GP terminó y los datos están disponibles en FastF1
- [ ] Explorar los datos de la sesión antes de ingestar

### Obtener el session_key de OpenF1
```
https://api.openf1.org/v1/sessions?meeting_key=XXXX&session_name=Race
https://api.openf1.org/v1/meetings?year=2026
```

### Actualizar `CARRERAS_2026` en `fetch_fastf1.py`
- [ ] Agregar el GP nuevo con su `session_key`
- [ ] Si es sprint weekend, agregar también las sesiones Sprint y SQ

### Correr el script
```bash
python3 ingestion/fetch_fastf1.py
```

### Validar en Supabase
- [ ] Verificar filas nuevas en `race_results`, `laps`, `pit_stops`, `qualifying_results`
- [ ] Verificar que los conteos son correctos (no duplicados, no filas faltantes)
- [ ] Actualizar `compound_in` y `compound_out` en `pit_stops` si es necesario

### Limpiar y documentar
- [ ] Limpiar el caché de FastF1: `rm -rf cache/*`
- [ ] Exportar CSVs para Tableau desde Supabase
- [ ] Actualizar dashboard en Tableau Public
- [ ] Commit y push:
```bash
git add .
git commit -m "data: add [nombre GP] 2026 results"
git push origin main
```

---

## GPs sprint 2026
- China (Round 2)
- Miami (Round 6)
- Canadá (Round 9)
- Gran Bretaña (Round 13)
- Países Bajos (Round 17)
- Singapur (Round 19)

---

## Carga histórica (temporadas pasadas)

Para ingestar una temporada completa el flujo es distinto al de carrera a carrera porque el volumen es demasiado grande para insertar via Python directamente en Supabase.

### Paso 1: Exportar datos crudos de FastF1
```bash
python3 ingestion/export_to_csv.py
```
Genera carpetas en `data/processed/YYYY_nombre_gp/` con `race_results.csv`, `laps.csv` y `qualifying.csv`.

### Paso 2: Transformar para Supabase
Primero exportar los catálogos desde Supabase:
```sql
SELECT driver_id, code, driver_number FROM drivers;
SELECT session_id, race_id, type FROM sessions;
SELECT race_id, name, season FROM races;
```
Guardar como `data/processed/drivers.csv`, `sessions.csv` y `races.csv`.
```bash
python3 ingestion/transform_for_supabase.py
```
Genera `all_race_results_YYYY.csv`, `all_laps_YYYY.csv` y `all_qualifying_YYYY.csv`.

### Paso 3: Exportar pit stops
```bash
python3 ingestion/export_pit_stops.py
```
Genera `all_pit_stops_YYYY.csv`.

### Paso 4: Importar a Supabase via UI
En este orden: `race_results` → `qualifying_results` → `laps` → `pit_stops`.

Table Editor → Insert → Import data from CSV.

### Paso 5: Limpiar archivos temporales
```bash
rm -rf data/processed/
mkdir -p data/processed data/raw
```

---

## Pendiente
- [ ] China 2026 (sprint weekend)
- [ ] `driver_standings` y `constructor_standings`
- [ ] Dashboard Tableau