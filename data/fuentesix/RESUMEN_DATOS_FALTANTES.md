# 📊 Resumen de Datos Faltantes - Base de Datos DELIA

**Fecha**: 2025-01-27  
**Total Obras en DB**: 2,100  
**Fuente de Análisis**: Fuentes IX (Varey & Shergold) - Textos extraídos

---

## 🎯 Datos Críticos Faltantes (Prioridad ALTA)

### 1. MECENAS 🔴
- **Estado actual**: ~5% de obras tienen mecenas
- **Objetivo**: Aumentar a >25% (+500 registros)
- **Fuente**: Fuentes IX contiene múltiples referencias a:
  - Reyes, reinas, príncipes
  - Fiestas palaciegas (cumpleaños, santos, nacimientos)
  - Títulos nobiliarios (Conde de Monterrey, etc.)
  - Organizadores (Heliche, etc.)

### 2. REPRESENTACIONES 🔴
- **Estado actual**: ~50% de obras tienen representaciones documentadas
- **Objetivo**: Aumentar a >80% (+1000 representaciones)
- **Datos a extraer**:
  - Fecha de representación
  - Compañía teatral
  - Lugar específico
  - Tipo de función (fiesta, celebración, normal)
  - Público (corte, pueblo, privado)

### 3. LUGARES 🔴
- **Estado actual**: ~40% de representaciones tienen lugar específico
- **Objetivo**: Aumentar a >80%
- **Lugares conocidos en Fuentes IX**:
  - Palacios: Alcázar, Buen Retiro, Cuarto del Rey, Cuarto de la Reina, Salón, Coliseo, etc.
  - Corrales: Corral del Príncipe, Corral de la Cruz
  - Otras ciudades: Valladolid, Toledo, El Pardo

### 4. COMPAÑÍAS TEATRALES 🟡
- **Estado actual**: ~50% tienen compañía identificada
- **Objetivo**: Normalizar y aumentar a >90%
- **Compañías frecuentes**: Manuel de Mosquera, Agustín Manuel, Manuel Vallejo, José de Prado, Jerónimo García, Rosendo López, Simón Aguado, Damián Polope, etc.

---

## 📋 Datos Secundarios Faltantes (Prioridad MEDIA)

### 5. FECHAS DE CREACIÓN 🟡
- **Estado actual**: ~30% tienen fecha estimada
- **Objetivo**: Aumentar a >45% (+300 fechas)
- **Fuentes**: Referencias a "comedia nueva", ediciones, manuscritos con fecha

### 6. EDICIONES PRÍNCIPES 🟢
- **Estado actual**: ~15% tienen información
- **Objetivo**: Aumentar a >25% (+200 ediciones)
- **Fuentes**: Referencias a Partes de dramaturgos, colecciones (Diferentes, Escogidas)

### 7. MANUSCRITOS CONOCIDOS 🟢
- **Estado actual**: ~10% tienen información
- **Objetivo**: Aumentar a >20%
- **Fuentes**: Referencias a bibliotecas y signaturas

### 8. TÍTULOS ALTERNATIVOS 🟢
- **Estado actual**: ~20% tienen títulos alternativos
- **Objetivo**: Identificar relaciones entre títulos
- **Ejemplos**: "Psiquis y Cupido" = "Ni amor se libra de amor"

---

## 📊 Estadísticas por Campo

| Campo | Completitud Actual | Objetivo | Registros Faltantes Estimados |
|-------|-------------------|----------|------------------------------|
| **Título** | ✅ 100% | 100% | 0 |
| **Autor** | ⚠️ 60% | 80% | ~400 |
| **Tipo de Obra** | ✅ 100% | 100% | 0 |
| **Género** | ⚠️ 20% | 40% | ~400 |
| **Subgénero** | ⚠️ 15% | 30% | ~300 |
| **Tema** | ⚠️ 10% | 25% | ~300 |
| **Fecha Creación** | ⚠️ 30% | 45% | ~300 |
| **Mecenas** | ❌ 5% | 25% | **~500** |
| **Lugares** | ⚠️ 40% | 80% | **~800** |
| **Representaciones** | ⚠️ 50% | 80% | **~1000** |
| **Compañías** | ⚠️ 50% | 90% | ~800 |
| **Edición Príncipe** | ⚠️ 15% | 25% | ~200 |
| **Manuscritos** | ⚠️ 10% | 20% | ~200 |

---

## 🎯 Plan de Acción por Fases

### **FASE 1: MECENAS** (Prioridad MÁXIMA)
- **Archivos**: part_001 a part_003
- **Tiempo estimado**: 2-3 horas de procesamiento IA
- **Resultado esperado**: +500 registros de mecenas
- **Impacto**: Alto - Datos únicos de Fuentes IX

### **FASE 2: LUGARES Y REPRESENTACIONES** (Prioridad MÁXIMA)
- **Archivos**: part_001 a part_006
- **Tiempo estimado**: 4-5 horas
- **Resultado esperado**: +1000 representaciones, +50 lugares únicos
- **Impacto**: Alto - Base para análisis geográfico y temporal

### **FASE 3: COMPAÑÍAS** (Prioridad ALTA)
- **Archivos**: Todos (part_001 a part_011)
- **Tiempo estimado**: 2 horas
- **Resultado esperado**: Normalización completa de compañías
- **Impacto**: Medio-Alto - Mejora filtros y búsquedas

### **FASE 4: FECHAS** (Prioridad ALTA)
- **Archivos**: Todos
- **Tiempo estimado**: 2 horas
- **Resultado esperado**: +300 fechas de creación
- **Impacto**: Medio - Mejora análisis cronológico

### **FASE 5: EDICIONES Y MANUSCRITOS** (Prioridad MEDIA)
- **Archivos**: Todos
- **Tiempo estimado**: 3 horas
- **Resultado esperado**: +200 ediciones príncipes, +200 manuscritos
- **Impacto**: Medio - Datos bibliográficos valiosos

### **FASE 6: TÍTULOS ALTERNATIVOS** (Prioridad MEDIA)
- **Archivos**: Todos
- **Tiempo estimado**: 1 hora
- **Resultado esperado**: Relaciones entre títulos
- **Impacto**: Bajo-Medio - Mejora identificación de obras

---

## 📈 Impacto Esperado Total

### Después de Completar Todas las Fases:

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Obras con datos completos** | ~20% | ~60% | +200% |
| **Representaciones totales** | ~1,050 | ~3,000+ | +185% |
| **Lugares únicos** | ~50 | ~100+ | +100% |
| **Mecenas identificados** | ~100 | ~600+ | +500% |
| **Valor académico** | Medio | **Alto** | ⬆️⬆️ |

---

## ⚠️ Consideraciones Importantes

1. **Calidad sobre Cantidad**: Mejor dejar campo vacío que inventar datos
2. **Confianza**: Siempre marcar nivel de confianza (alto/medio/bajo)
3. **Trazabilidad**: Incluir página PDF y texto original
4. **Discrepancias**: Documentar discrepancias entre fuentes
5. **Normalización**: Usar nombres normalizados pero conservar originales

---

## 📚 Documentos de Referencia

- **Plan Completo**: `PLAN_EXTRACCION_IA_FUENTES_IX.md`
- **Ejemplos Concretos**: `EJEMPLOS_EXTRACCION_FUENTES_IX.md`
- **Estructura DB**: `apps/obras/models.py`, `apps/representaciones/models.py`
- **Metadatos Geográficos**: `geographic_metadata.json`
- **Lugares Procesados**: `lugares_procesados.json`

---

**Próximos Pasos**:
1. Revisar documentos de referencia
2. Configurar procesamiento IA con instrucciones precisas
3. Ejecutar Fase 1 (Mecenas) como prueba piloto
4. Validar resultados antes de continuar
5. Proceder con fases siguientes

---

**Última actualización**: 2025-01-27






