# 📚 Lemario de Términos - Fuentes IX

## 🎯 Propósito

Este documento contiene el lemario (colección de términos) extraído automáticamente de los textos de Fuentes IX, junto con las frases donde aparecen y patrones de detección sugeridos.

---

## 📊 Resumen Ejecutivo

- **Total de frases analizadas**: 116
- **Términos únicos identificados**: 401
- **Frases completas** (con 3+ elementos): 26

---

## 🔍 Términos por Categoría

### MECENAS (6 términos únicos, 40 ocurrencias)

| Término | Ocurrencias | Ejemplo de Contexto |
|---------|-------------|---------------------|
| Reina | 19 | "...para festejar el cumpleaños de la Reina María Luisa de Borbón..." |
| Príncipe | 12 | "...en el Cuarto de Príncipes..." |
| Rey | 6 | "...representaciones en los palacios reales..." |
| La Reina Madre | 1 | "...para celebrar el santo de la Reina Madre..." |
| Conde | 1 | "...el Conde de Monterrey comenta..." |

**Patrones de Detección**:
- `para festejar el [evento] de [MECENAS]`
- `para celebrar el [evento] de [MECENAS]`
- `representó a [MECENAS]`
- `en honor de [MECENAS]`

---

## 📅 Patrones de Fecha Detectados

### Formato más común: `dia de mes de año`
- Ejemplo: "22 de enero de 1687"
- Regex sugerido: `(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})`

### Otros formatos encontrados:
- **Rangos**: "10-13 de mayo de 1696"
- **Antes de**: "antes del 30 de enero de 1688"
- **Entre**: "Entre 5 de octubre de 1622 y 8 de febrero de 1623"
- **Solo año**: "1687"

---

## 🏛️ Lugares Más Frecuentes

| Lugar | Frecuencia | Variantes |
|-------|------------|-----------|
| Palacio | 77 | Alcázar, Palacio Real |
| Buen Retiro | 31 | Real Retiro, Retiro |
| Cuarto de la Reina | 15 | Cuarto Reina |
| Salón | 15 | Salón dorado |
| Corral del Príncipe | 13 | Príncipe |
| Corral de la Cruz | 8 | Cruz |
| Saloncete | 5 | Saloncillo |

**Patrones de Detección**:
- `en [LUGAR]`
- `[LUGAR], [sala específica]`
- `representación palaciega` → implica Palacio o Buen Retiro

---

## 🎭 Compañías Más Frecuentes

| Compañía | Frecuencia | Variantes |
|----------|------------|-----------|
| Manuel de Mosquera | 13 | Mosquera, Manuel Mosquera |
| Simón Aguado | 15 | Aguado |
| Manuel Vallejo | 17 | Vallejo, Manuel de Vallejo |
| Jerónimo García | 4 | García |
| Agustín Manuel | 4 | Manuel |
| Rosendo López | 8 | López |
| Damián Polope | 4 | Polope, Polop |

**Patrones de Detección**:
- `compañía de [NOMBRE]`
- `[NOMBRE]. Palacio` (nombre seguido de punto y lugar)
- `[NOMBRE] y [NOMBRE]` (múltiples compañías)

---

## 📝 Frases Completas (Ejemplos)

Frases que contienen fecha + compañía + lugar + obra:

1. **"El 22 de mayo de 1687 la compañía de Agustín Manuel representó El Pastor Fido, en el Saloncillo del Buen Retiro"**
   - Fecha: 22 de mayo de 1687
   - Compañía: compañía de Agustín Manuel
   - Lugar: Saloncillo del Buen Retiro
   - Obra: El Pastor Fido

2. **"9 de enero de 1681. Jerónimo García. Palacio"**
   - Fecha: 9 de enero de 1681
   - Compañía: Jerónimo García
   - Lugar: Palacio

3. **"18 de enero de 1678. Agustín Manuel y Antonio Escamilla. Palacio"**
   - Fecha: 18 de enero de 1678
   - Compañía: Agustín Manuel y Antonio Escamilla (múltiples)
   - Lugar: Palacio

---

## 🎯 Patrones de Representación Generados

### Patrón 1: Representación completa con múltiples elementos
```
[FECHA]. [COMPAÑÍA]. [LUGAR] ([FUENTE])
```

### Patrón 2: Representación con obra explícita
```
[FECHA] la compañía de [COMPAÑÍA] representó [OBRA], en [LUGAR]
```

### Patrón 3: Representación con mecenas
```
[FECHA] ... para festejar/celebrar [EVENTO] de [MECENAS]
```

---

## 💡 Recomendaciones para Mejora

1. **Normalización de nombres**: Crear diccionario de variantes
   - "Manuel de Mosquera" = "Mosquera" = "Manuel Mosquera"

2. **Detección de obras**: Mejorar patrones para títulos de obras
   - Buscar después de "representó", "hizo", "comedia"

3. **Lugares compuestos**: Detectar mejor lugares con múltiples partes
   - "Buen Retiro, Coliseo"
   - "Palacio, Salón dorado"

4. **Fechas especiales**: Manejar mejor fechas especiales
   - "Lunes de Carnestolendas de 1657 (12 de febrero)"
   - "antes del X de Y de Z"

---

## 📈 Próximos Pasos

1. ✅ Sistema de extracción inteligente creado
2. ✅ Lemario inicial generado
3. ⏳ Mejorar patrones de detección basados en ejemplos
4. ⏳ Crear diccionario de normalización de términos
5. ⏳ Generar reglas de extracción automáticas

---

**Última actualización**: 2025-01-27
**Archivos analizados**: part_001, part_003






