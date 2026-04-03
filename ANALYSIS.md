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

**Visualización:** Tableau - Sheet Tyre Degradation

**Metodología:** 
Se filtran vueltas con `is_accurate = true` y compuestos válidos (SOFT, MEDIUM, HARD, INTERMEDIATE, WET).
FastF1 excluye automáticamente safety car, pit laps y vueltas anómalas.
Esto representa el 83% de las vueltas totales (hasta China 2026), equivalente a 2172 filas limpias.

**Ejemplo: Australia 2025 - Gasly**
- INTERMEDIATE: tendencia negativa (-1.11s por vuelta), R²=0.66, p<0.0001
  - Las intermedias mejoran con el uso porque generan temperatura progresivamente
- HARD: comportamiento irregular con pocas vueltas, difícil de interpretar

**Insight:** 
La línea de tendencia lineal con R²=0.66 confirma que el desgaste de goma explica 
el 65% de la variación en los tiempos de vuelta. La relación es estadísticamente 
significativa (p<0.0001), no es ruido aleatorio.

**Limitación:** 
Los tiempos varían vuelta a vuelta por factores externos (tráfico, temperatura, viento).
Con pocos datos por stint el promedio es sensible a vueltas irregulares.
Se necesitan al menos 10 vueltas por stint para tendencias confiables.

**Próximos pasos:** Comparar degradación de Alpine vs midfield en las mismas carreras.


### 4. Gap to Pole Position 2025-2026
**Query:** sql/gap_to_pole.sql

**Resultado:** Gasly consistentemente más cerca del pole que sus compañeros.

**Insight:** Mejor resultado de Gasly fue Bahrain 2025 a 0.375s del pole. 
Las Vegas fue el peor fin de semana para Alpine con COL a 5.749s.

**Próximos pasos:** Analizar si hay correlación entre gap al pole y tipo de circuito.


### 5. Tyre Usage by Race 2025-2026
**Query:** sql/tyre_usage.sql

**Resultado:** Alpine usó principalmente HARD y MEDIUM en 2025. SOFT aparece en pocas carreras.

**Insight:** Alpine prefirió estrategias conservadoras con compuestos duros durante 2025.

**Limitación:** Solo stints con datos completos (is_accurate = true).

**Próximos pasos:** Analizar stint length promedio por compuesto cuando haya más datos de 2026.

### 6. Tyre Strategy vs Midfield 2025-2026
**Query:** sql/midfield_tyre_strategy.sql

**Resultado:** Alpine tiene stints más cortos que Kick Sauber/Audi pero comparables con Haas y Williams.

**Insight:** La estrategia de gomas de Alpine no es un diferenciador claro respecto al midfield. El rendimiento en carrera refleja más el ritmo del auto que decisiones estratégicas.

**Limitación:** Stints calculados con is_accurate=true, lo que puede subestimar la duración real en carreras con safety car o lluvia.


### 7. Pit Stop Position Change 2025-2026
**Query:** sql/pit_stop_position_change.sql

**Resultado:** Alpine pierde posiciones en la mayoría de las paradas. El promedio es negativo en casi todas las carreras.

**Insight:** Perder posiciones al parar es normal en F1 cuando largás desde el fondo. El dato más relevante es cuántas posiciones se recuperan después de la parada, no cuántas se pierden en el momento.

**Limitación:** Las carreras con conditions=mixed pueden incluir paradas reactivas al clima que no reflejan decisiones estratégicas.