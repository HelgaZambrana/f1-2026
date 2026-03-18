# F1 Alpine Analysis - 2025/2026

## Contexto
Análisis del rendimiento del equipo Alpine en las temporadas 2025 y 2026.
Pilotos: Gasly (toda la temporada 2025 y 2026), Doohan (rondas 1-7 2025), Colapinto (rondas 8-24 2025 y 2026).

---

## Análisis exploratorio

### 1. Alpine Race Performance 2025-2026
**Query:** sql/race_performances.sql
**Resultado:** Alpine terminó mayormente entre 13vo y 20vo en 2025. En 2026 mejora a 6to-14vo.
**Insight:** El problema en 2025 era el auto, no los pilotos. En 2026 el equipo muestra una mejora significativa en posicionamiento relativo.


### 2. Alpine Qualifying Performance 2025-2026
**Query:** sql/qualifying_comparison.sql
**Resultado:**
- Gasly llegó consistentemente a Q2/Q3 durante 2025, siendo el mejor Alpine en qualifying en la mayoría de las carreras
- En 2025, Colapinto se quedó en Q1 en la mayoría de sus carreras, con excepciones en Canadá, Austria, Hungría, Las Vegas y EEUU (Texas) donde llegó a Q2
- Doohan superó a Gasly en Q1 en Miami y Bahrain, sugiriendo que era competitivo en clasificación
- En China 2026 Colapinto fue el mejor Alpine en Q1 y estuvo a solo 0.005s del décimo puesto en Q2
**Insights:**
- El problema de clasificación de Alpine en 2025 era principalmente el auto, no los pilotos
- Colapinto muestra mejora clara en qualifying entre 2025 y 2026
- Gasly es consistentemente el pilar del equipo en clasificación
**Próximos pasos:** Analizar si los circuitos donde Colapinto llegó a Q2 coinciden con sus mejores resultados de carrera


### 3. Alpine Tyre Degradation 2025-2026
**Query:** sql/tyre_analysis.sql
**Metodología:** Se filtran vueltas con `is_accurate = true` 
(FastF1 excluye automáticamente safety car, pit laps y vueltas anómalas).
Esto representa el 83% de las vueltas totales (hasta China 2026).
**Resultado:** Hasta China 2026, 2172 filas de vueltas limpias para análisis de degradación.
**Limitación:** Los tiempos varían vuelta a vuelta por factores externos 
(tráfico, temperatura, viento). La tendencia se visualiza mejor con una 
línea de regresión en Tableau.
**Próximos pasos:** Visualizar en Tableau con línea de tendencia por compuesto.