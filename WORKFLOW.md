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
6. Siempre cachear los driver IDs localmente al inicio del script, nunca consultar Supabase por cada vuelta

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
- [ ] Agregar el GP nuevo con su `session_key`, `sprint_key` y `sq_key`
- [ ] Si no es sprint weekend, poner `None` en `sprint_key` y `sq_key`

### Correr el script
```bash
python3 ingestion/fetch_fastf1.py
```
- El script reconecta Supabase en cada carrera automáticamente
- Si el sprint no tiene pit stops OpenF1 devuelve 404, el script lo maneja solo

### Validar en Supabase
- [ ] Verificar filas nuevas en `race_results`, `laps`, `pit_stops`, `qualifying_results`
- [ ] Verificar que los conteos son correctos (no duplicados, no filas faltantes)
- [ ] Actualizar `compound_in` y `compound_out` en `pit_stops`

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
- China (Round 2) ✓
- Miami (Round 6)
- Canadá (Round 9)
- Gran Bretaña (Round 13)
- Países Bajos (Round 17)
- Singapur (Round 19)

---

## Campos calculados por FastF1

### is_accurate
Booleano que indica si una vuelta es confiable para análisis. FastF1 lo calcula cruzando el estado de la pista con los datos de timing. Excluye automáticamente safety car, pit laps y vueltas anómalas. Usar siempre como filtro en queries de degradación de gomas.

### track_status
Estado de la pista en esa vuelta. Valores principales:
- `1` → pista verde
- `4` → safety car
- `6` → safety car virtual
- `7` → bandera roja

---

## CSVs por dashboard

### Dashboard 1: Race Overview
| CSV | Query |
|---|---|
| `race_performance.csv` | `sql/race_performance.sql` |
| `alpine_driver_cards.csv` | `sql/alpine_driver_cards.sql` |

### Dashboard 2: Qualifying Overview
| CSV | Query |
|---|---|
| `qualifying_comparison.csv` | `sql/qualifying_comparison.sql` |
| `qualy_kpi.csv` | `sql/qualy_kpi.sql` |
| `alpine_teammate_gap.csv` | `sql/alpine_teammate_gap.sql` |
| `gap_to_pole.csv` | `sql/gap_to_pole.sql` |

### Dashboard 3: Tyre Strategy
| CSV | Query |
|---|---|
| `tyre_analysis.csv` | `sql/tyre_analysis.sql` |
| `tyre_usage_with_images.csv` | `sql/tyre_usage.sql` |
| `midfield_tyre_strategy.csv` | `sql/midfield_tyre_strategy.sql` |
| `pit_stop_position_change.csv` | `sql/pit_stop_position_change.sql` |