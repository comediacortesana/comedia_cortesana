# 📊 Sistema de Análisis e Interpretaciones de IA - Fuentes IX

## 🎯 Objetivo

Crear un sistema similar a los comentarios pero específico para guardar:
- **Frases originales** donde la IA encontró datos
- **Interpretaciones** de la IA sobre esos datos
- **Discrepancias** detectadas entre fuentes
- **Patrones** que llevaron a la extracción
- **Contexto adicional** para entender mejor los datos

---

## 🏗️ Estructura

### Tabla: `analisis_ia_fuentes_ix`

Similar a `comentarios` pero específico para análisis de IA:

```sql
CREATE TABLE analisis_ia_fuentes_ix (
    id UUID PRIMARY KEY,
    tipo_registro VARCHAR(50), -- 'obra', 'representacion', 'lugar', 'mecenas'
    registro_id VARCHAR(200), -- ID del registro (puede ser temporal)
    
    -- Contenido del análisis
    datos_extraidos JSONB, -- Resumen de datos extraídos
    frases_originales JSONB, -- Array de frases donde se encontraron
    interpretaciones JSONB, -- Array de interpretaciones de la IA
    discrepancias JSONB, -- Array de discrepancias detectadas
    patrones_detectados JSONB, -- Array de patrones usados
    
    -- Metadata
    confianza VARCHAR(20), -- 'alto', 'medio', 'bajo'
    archivo_fuente VARCHAR(200),
    pagina_pdf INTEGER,
    fuente_ia VARCHAR(100),
    version_ia VARCHAR(20),
    
    -- Estado
    estado VARCHAR(50), -- 'pendiente_revision', 'revisado', 'integrado'
    revisado_por UUID,
    revisado_at TIMESTAMPTZ
);
```

---

## 📝 Ejemplo de Uso

### Análisis de Representación con Discrepancia

```json
{
  "tipo": "analisis_ia_fuentes_ix",
  "tipo_registro": "representacion",
  "registro_id": "temp_part_001_rep_1",
  "datos_extraidos": {
    "obra_titulo": "El Pastor Fido",
    "fecha": "22 de mayo de 1687",
    "compañia": "compañía de Agustín Manuel",
    "lugar": "Saloncillo del Buen Retiro"
  },
  "frases_originales": [
    "El 22 de mayo de 1687 la compañía de Agustín Manuel representó El Pastor Fido, en el Saloncillo del Buen Retiro, según Fuentes V",
    "y en el Saloncete, según Fuentes I"
  ],
  "interpretaciones": [
    "Ambas fuentes mencionan la misma representación pero con nombres diferentes de sala",
    "Saloncillo y Saloncete son ambas salas del Buen Retiro, probablemente la misma representación"
  ],
  "discrepancias": [
    {
      "tipo": "lugar",
      "fuente_1": {"fuente": "Fuentes I", "lugar": "Saloncete"},
      "fuente_2": {"fuente": "Fuentes V", "lugar": "Saloncillo del Buen Retiro"},
      "resolucion": "Ambas son salas del Buen Retiro"
    }
  ],
  "patrones_detectados": [
    "[FECHA] la compañía de [COMPAÑÍA] representó [OBRA], en [LUGAR], según [FUENTE]"
  ],
  "confianza": "medio",
  "archivo_fuente": "part_001",
  "pagina_pdf": 134
}
```

---

## 🔄 Flujo de Trabajo

### 1. Extracción de Datos
```python
# Procesar texto y extraer datos
datos_extraidos = extraer_datos(texto)
```

### 2. Generar Análisis de IA
```python
analisis_ia = AnalisisIA()
analisis = analisis_ia.crear_analisis_registro(
    tipo_registro='representacion',
    datos_extraidos=datos_extraidos,
    frases_originales=[frase1, frase2],
    interpretaciones=["Interpretación 1", "Interpretación 2"],
    discrepancias=[discrepancia1],
    confianza='medio'
)
```

### 3. Guardar en DB
```python
# Guardar análisis en Supabase
guardar_analisis_ia(analisis)
```

### 4. Revisión Manual
- Admin/Editor revisa análisis pendientes
- Marca como 'revisado' o 'integrado'
- Puede añadir notas de revisión

---

## 🎨 Visualización en Frontend

Similar a comentarios pero con:
- Badge "IA" para identificar análisis automáticos
- Mostrar frases originales en tooltip o expandible
- Mostrar discrepancias destacadas
- Mostrar nivel de confianza con colores:
  - 🟢 Alto (verde)
  - 🟡 Medio (amarillo)
  - 🔴 Bajo (rojo)

---

## 📊 Tipos de Análisis

### 1. Análisis General (`analisis_ia_fuentes_ix`)
- Análisis completo de un registro
- Incluye frases, interpretaciones, discrepancias

### 2. Discrepancia Específica (`discrepancia_fuentes`)
- Análisis enfocado en una discrepancia entre fuentes
- Compara fuente_1 vs fuente_2
- Incluye interpretación y resolución sugerida

### 3. Patrón Detectado (`patron_deteccion`)
- Patrón identificado automáticamente
- Ejemplos donde se encontró
- Confianza del patrón

### 4. Frase con Contexto (`frase_contexto`)
- Análisis de una frase específica
- Términos identificados
- Contexto anterior y posterior

---

## 🔍 Ventajas

1. **Trazabilidad**: Saber exactamente de dónde vienen los datos
2. **Transparencia**: Ver qué interpretó la IA y por qué
3. **Revisión**: Poder revisar y corregir interpretaciones
4. **Aprendizaje**: Los patrones detectados mejoran futuras extracciones
5. **Confianza**: Niveles de confianza ayudan a priorizar revisión

---

## 📋 Próximos Pasos

1. ✅ Estructura de tabla creada
2. ✅ Scripts de generación de análisis creados
3. ⏳ Integrar con sistema de extracción
4. ⏳ Crear interfaz de visualización en frontend
5. ⏳ Sistema de revisión para admins

---

**Última actualización**: 2025-01-27






