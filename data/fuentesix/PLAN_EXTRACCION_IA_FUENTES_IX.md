# 📋 Plan de Extracción de Datos con IA - Fuentes IX

## 📊 Resumen Ejecutivo

**Fuente**: FUENTES IX - "Comedias en Madrid: 1603-1709" (Varey & Shergold)  
**Archivos de texto**: 11 archivos (`part_001` a `part_011`)  
**Objetivo**: Extraer datos estructurados para completar la base de datos DELIA  
**Estructura DB**: Compatible con modelos Django existentes (Obra, Representacion, Lugar)

---

## 🔍 Análisis de Datos Faltantes

### Estado Actual de la Base de Datos (2100 obras)

| Campo | % Completitud Estimada | Prioridad |
|-------|----------------------|-----------|
| **Título** | ✅ 100% | Alta |
| **Autor** | ⚠️ ~60% | Alta |
| **Tipo de Obra** | ✅ 100% | Media |
| **Género/Subgénero** | ⚠️ ~20% | Media |
| **Tema** | ⚠️ ~10% | Media |
| **Fecha de Creación** | ⚠️ ~30% | Alta |
| **Mecenas** | ❌ ~5% | **ALTA** |
| **Lugares** | ⚠️ ~40% | **ALTA** |
| **Representaciones** | ⚠️ ~50% | **ALTA** |
| **Compañías** | ⚠️ ~50% | Alta |
| **Edición Príncipe** | ⚠️ ~15% | Media |
| **Manuscritos Conocidos** | ⚠️ ~10% | Media |
| **Notas Bibliográficas** | ⚠️ ~20% | Baja |

---

## 🎯 Tareas de Extracción (Orden de Prioridad)

### **TAREA 1: MECENAS** 🔴 PRIORIDAD MÁXIMA

#### Objetivo
Extraer información sobre mecenas, patrocinadores y organizadores de representaciones.

#### Campos a Extraer
- **Campo DB**: `mecenas` (Obra) y `mecenas` (Representacion)
- **Campo DB**: `organizadores_fiesta` (Representacion)
- **Campo DB**: `personajes_historicos` (Representacion)

#### Instrucciones para IA

```
INSTRUCCIONES PARA EXTRACCIÓN DE MECENAS Y PATROCINADORES

1. BUSCAR PATRONES:
   - "para celebrar el [evento] de [persona]"
   - "festejar el [evento] de [persona]"
   - "en honor de [persona/título]"
   - "por orden de [persona/título]"
   - "mandó [persona/título]"
   - "para el [evento] de [persona]"
   - Menciones de reyes, reinas, príncipes, nobles, embajadores
   - Títulos nobiliarios: Conde, Duque, Marqués, etc.

2. CONTEXTO ESPECÍFICO DE FUENTES IX:
   - Representaciones palaciegas: buscar menciones a reyes, reinas, príncipes
   - Fiestas reales: cumpleaños, santos, nacimientos, recuperación de salud
   - Ejemplos del texto:
     * "para festejar el cumpleaños del Rey"
     * "el santo de la Reina"
     * "el nacimiento de un Príncipe"
     * "la recuperación de la salud de un miembro de la familia real"
     * "para celebrar el santo de la Reina Madre"
     * "el Conde de Monterrey"
     * "Heliche" (organizador de fiestas)

3. FORMATO DE SALIDA (JSON):
   {
     "obra_id": "ID de la obra si se puede identificar",
     "titulo_obra": "Título de la obra",
     "mecenas": "Nombre del mecenas o patrocinador principal",
     "organizadores": ["Lista de organizadores si hay múltiples"],
     "personajes_historicos": ["Nombres de personajes históricos mencionados"],
     "motivo": "Razón de la representación (cumpleaños, santo, etc.)",
     "fecha": "Fecha de la representación si está disponible",
     "lugar": "Lugar de la representación",
     "pagina_pdf": "Número de página donde aparece",
     "texto_original": "Fragmento del texto original que contiene la información",
     "confianza": "alto|medio|bajo"
   }

4. REGLAS DE EXTRACCIÓN:
   - Si se menciona "Rey" sin nombre específico → "Rey de España" o "Felipe IV" según contexto
   - Si se menciona "Reina" → identificar si es "María Luisa de Borbón", "Mariana de Austria", etc.
   - Títulos nobiliarios: extraer completo ("Conde de Monterrey", no solo "Monterrey")
   - Si hay múltiples mecenas, listar todos
   - Si es una fiesta organizada por alguien específico, incluir en "organizadores"

5. CASOS ESPECIALES:
   - "representación palaciega" → mecenas probablemente es la corte real
   - "representación al pueblo" → puede no tener mecenas específico
   - Menciones a "Heliche" → es un organizador importante de fiestas palaciegas
   - Gremios o cofradías → incluir como organizadores

6. VALIDACIÓN:
   - Verificar que el nombre extraído es una persona/título, no un lugar
   - Verificar coherencia temporal (personas que existían en la fecha mencionada)
   - Si hay duda, marcar confianza como "medio" o "bajo"
```

#### Ejemplo de Salida Esperada

```json
{
  "obra_id": null,
  "titulo_obra": "La profetisa Casandra",
  "mecenas": "María Luisa de Borbón",
  "organizadores": ["Heliche"],
  "personajes_historicos": ["Reina María Luisa de Borbón"],
  "motivo": "festejar el cumpleaños de la Reina",
  "fecha": "21 de septiembre de 1685",
  "lugar": "Palacio",
  "pagina_pdf": 135,
  "texto_original": "proyectada para festejar el cumpleaños de la Reina María Luisa de Borbón",
  "confianza": "alto"
}
```

---

### **TAREA 2: LUGARES Y REPRESENTACIONES** 🔴 PRIORIDAD MÁXIMA

#### Objetivo
Extraer información completa sobre lugares de representación y crear registros de representaciones.

#### Campos a Extraer
- **Lugar**: `nombre`, `tipo_lugar`, `region`, `coordenadas` (si aplica)
- **Representación**: `fecha`, `compañia`, `lugar`, `tipo_lugar`, `tipo_funcion`, `publico`, `mecenas`, `observaciones`

#### Instrucciones para IA

```
INSTRUCCIONES PARA EXTRACCIÓN DE LUGARES Y REPRESENTACIONES

1. LUGARES ESPECÍFICOS DE FUENTES IX:

   PALACIOS:
   - "Palacio" o "Alcázar" → Palacio Real de Madrid
   - "Buen Retiro" → Palacio del Buen Retiro
   - "Cuarto del Rey" → dentro del Palacio Real
   - "Cuarto de la Reina" → dentro del Palacio Real
   - "Cuarto de Príncipes" → dentro del Buen Retiro
   - "Salón" o "Salón dorado" → Palacio Real
   - "Pieza de las Audiencias" → Palacio Real
   - "Armería" → Palacio Real
   - "Coliseo" → Buen Retiro
   - "Saloncete", "Saloncillo", "Salón de los Reinos" → Buen Retiro
   - "Patinejo" → Buen Retiro
   - "Palacio Real de El Pardo" → El Pardo
   
   CORRALES:
   - "Corral del Príncipe" → Madrid, Calle del Príncipe
   - "Corral de la Cruz" → Madrid, Calle de la Cruz
   
   OTRAS CIUDADES:
   - "Valladolid" → Valladolid, Castilla y León
   - "Toledo" → Toledo, Castilla-La Mancha
   - "El Pardo" → El Pardo, Comunidad de Madrid

2. TIPOS DE REPRESENTACIÓN:
   - "representación palaciega" → tipo_lugar: "palacio", publico: "corte"
   - "representación al pueblo" → tipo_lugar: "corral", publico: "pueblo"
   - "particular" o "particulares" → representación privada
   - "ensayo" → no es representación final, pero documentar
   - "fiesta" o "festejo" → tipo_funcion: "fiesta"

3. FORMATO DE SALIDA (JSON):
   {
     "representaciones": [
       {
         "obra_titulo": "Título de la obra",
         "fecha": "Fecha original del texto (ej: '3 de octubre de 1685')",
         "fecha_formateada": "YYYY-MM-DD si se puede determinar",
         "compañia": "Nombre de la compañía teatral",
         "director_compañia": "Nombre del director si está disponible",
         "lugar_nombre": "Nombre del lugar",
         "lugar_tipo": "palacio|corral|iglesia|plaza|teatro|casa|universidad|convento|otro",
         "lugar_region": "Región o provincia",
         "lugar_ciudad": "Ciudad",
         "tipo_funcion": "fiesta|celebración|representación_normal|ensayo",
         "publico": "corte|pueblo|privado",
         "observaciones": "Información adicional sobre la representación",
         "pagina_pdf": "Número de página",
         "texto_original": "Fragmento del texto original",
         "confianza": "alto|medio|bajo"
       }
     ],
     "lugares_nuevos": [
       {
         "nombre": "Nombre del lugar",
         "tipo": "palacio|corral|etc",
         "region": "Región",
         "ciudad": "Ciudad",
         "descripcion": "Descripción si está disponible",
         "coordenadas": {"lat": null, "lng": null}
       }
     ]
   }

4. REGLAS DE EXTRACCIÓN:
   - Fechas: mantener formato original, pero intentar parsear a formato estándar
   - Compañías: buscar nombres como "compañía de [nombre]", "compañías de [nombre] y [nombre]"
   - Si hay múltiples compañías → separar con " y " o crear múltiples registros
   - Si el lugar no está especificado pero es "representación palaciega" → lugar: "Palacio"
   - Si hay discrepancias entre fuentes, documentar en observaciones

5. CASOS ESPECIALES:
   - "representación palaciega" sin lugar específico → usar "Palacio" (Alcázar)
   - Menciones a "representación al pueblo" → lugar probablemente es un corral
   - Fechas con discrepancias → documentar ambas en observaciones
   - Representaciones el mismo día → pueden ser válidas (dos comedias diferentes)
```

#### Ejemplo de Salida Esperada

```json
{
  "representaciones": [
    {
      "obra_titulo": "El Pastor Fido",
      "fecha": "22 de mayo de 1687",
      "fecha_formateada": "1687-05-22",
      "compañia": "Agustín Manuel",
      "director_compañia": "",
      "lugar_nombre": "Saloncillo del Buen Retiro",
      "lugar_tipo": "palacio",
      "lugar_region": "Comunidad de Madrid",
      "lugar_ciudad": "Madrid",
      "tipo_funcion": "representación_normal",
      "publico": "corte",
      "observaciones": "Según Fuentes V. Fuentes I menciona Saloncete.",
      "pagina_pdf": 134,
      "texto_original": "la compañía de Agustín Manuel representó El Pastor Fido, en el Saloncillo del Buen Retiro",
      "confianza": "medio"
    }
  ],
  "lugares_nuevos": []
}
```

---

### **TAREA 3: COMPAÑÍAS TEATRALES** 🟡 PRIORIDAD ALTA

#### Objetivo
Extraer y normalizar nombres de compañías teatrales y directores.

#### Campos a Extraer
- **Representacion**: `compañia`, `director_compañia`

#### Instrucciones para IA

```
INSTRUCCIONES PARA EXTRACCIÓN DE COMPAÑÍAS TEATRALES

1. PATRONES DE BÚSQUEDA:
   - "compañía de [nombre]"
   - "compañías de [nombre] y [nombre]"
   - "la compañía de [nombre]"
   - "compañía de [nombre] y [nombre]"
   - Nombres propios seguidos de "representó" o "hizo"

2. NORMALIZACIÓN:
   - Mantener formato: "compañía de [Nombre Apellido]"
   - Si hay dos compañías: "compañía de [Nombre1] y compañía de [Nombre2]"
   - Director = nombre del dueño/director de la compañía

3. COMPAÑÍAS CONOCIDAS EN FUENTES IX:
   - Manuel de Mosquera
   - Agustín Manuel
   - Manuel Vallejo
   - José de Prado
   - Jerónimo García
   - Rosendo López
   - Simón Aguado
   - Damián Polope
   - Manuel de Villaflor
   - Matías de Castro
   - Antonio García de Prado
   - Manuel de Vallejo

4. FORMATO DE SALIDA:
   {
     "compañias": [
       {
         "nombre_completo": "compañía de Manuel de Mosquera",
         "director": "Manuel de Mosquera",
         "variantes": ["Manuel de Mosquera", "Mosquera"],
         "fechas_activas": ["1684", "1685"],
         "obras_representadas": ["Lista de títulos"],
         "confianza": "alto|medio|bajo"
       }
     ]
   }
```

---

### **TAREA 4: FECHAS Y CRONOLOGÍA** 🟡 PRIORIDAD ALTA

#### Objetivo
Extraer y normalizar fechas de creación de obras y fechas de representaciones.

#### Campos a Extraer
- **Obra**: `fecha_creacion_estimada`
- **Representacion**: `fecha`, `fecha_formateada`

#### Instrucciones para IA

```
INSTRUCCIONES PARA EXTRACCIÓN DE FECHAS

1. FECHAS DE CREACIÓN:
   - Buscar menciones a "data de", "fecha de", "escrita en", "compuesta en"
   - Fechas límite: "antes de [fecha]", "después de [fecha]"
   - Referencias a ediciones: "edición de [año]"
   - Referencias a manuscritos con fecha

2. FECHAS DE REPRESENTACIÓN:
   - Formato común: "día de mes de año" (ej: "3 de octubre de 1685")
   - Formato alternativo: "día mes año" o variantes
   - Fechas aproximadas: "en [mes] de [año]", "durante [año]"

3. NORMALIZACIÓN:
   - Mantener fecha original en campo "fecha"
   - Intentar parsear a formato estándar en "fecha_formateada"
   - Si solo hay año: usar "YYYY-01-01" como aproximación
   - Si hay mes y año: usar "YYYY-MM-01"

4. CASOS ESPECIALES:
   - "comedia nueva" en [año] → puede indicar fecha de creación aproximada
   - Referencias a "diez años a esta parte" → calcular fecha relativa
   - Discrepancias entre fuentes → documentar ambas fechas
```

---

### **TAREA 5: EDICIONES Y MANUSCRITOS** 🟢 PRIORIDAD MEDIA

#### Objetivo
Extraer información sobre ediciones príncipes y manuscritos conocidos.

#### Campos a Extraer
- **Obra**: `edicion_principe`, `manuscritos_conocidos`, `ediciones_conocidas`, `notas_bibliograficas`

#### Instrucciones para IA

```
INSTRUCCIONES PARA EXTRACCIÓN DE EDICIONES Y MANUSCRITOS

1. EDICIÓN PRÍNCIPE:
   - Buscar: "edición príncipe", "primera edición", "edición de [año]"
   - Referencias a Partes de dramaturgos
   - Referencias a colecciones (Diferentes, Escogidas)

2. MANUSCRITOS:
   - Buscar: "manuscrito", "MS", "signatura", "Biblioteca [nombre]"
   - Referencias a catálogos de bibliotecas
   - Signaturas de manuscritos

3. FORMATO:
   {
     "edicion_principe": "Información completa sobre la edición príncipe",
     "manuscritos": [
       {
         "biblioteca": "Nombre de la biblioteca",
         "signatura": "Signatura del manuscrito",
         "fecha": "Fecha si está disponible",
         "descripcion": "Descripción adicional"
       }
     ],
     "ediciones_conocidas": "Lista de otras ediciones mencionadas",
     "notas_bibliograficas": "Notas adicionales sobre bibliografía"
   }
```

---

### **TAREA 6: TÍTULOS ALTERNATIVOS** 🟢 PRIORIDAD MEDIA

#### Objetivo
Identificar y relacionar títulos alternativos de obras.

#### Campos a Extraer
- **Obra**: `titulo_alternativo`

#### Instrucciones para IA

```
INSTRUCCIONES PARA EXTRACCIÓN DE TÍTULOS ALTERNATIVOS

1. PATRONES:
   - "también conocida como", "también llamada", "título alternativo"
   - Menciones de la misma obra con título diferente
   - Referencias cruzadas entre fuentes

2. EJEMPLOS DEL TEXTO:
   - "Psiquis y Cupido" = "Ni amor se libra de amor"
   - "Pitias y Damón" = "La amistad vence el rigor"
   - "El alcalde de Zalamea" = "El garroté más bien dado"

3. FORMATO:
   {
     "titulo_principal": "Título principal",
     "titulos_alternativos": ["Título alternativo 1", "Título alternativo 2"],
     "confianza": "alto|medio|bajo",
     "fuente": "Texto que relaciona los títulos"
   }
```

---

### **TAREA 7: GÉNEROS Y TEMAS** 🟢 PRIORIDAD BAJA

#### Objetivo
Extraer información sobre géneros, subgéneros y temas literarios.

#### Campos a Extraer
- **Obra**: `genero`, `subgenero`, `tema`

#### Instrucciones para IA

```
INSTRUCCIONES PARA EXTRACCIÓN DE GÉNEROS Y TEMAS

1. GÉNEROS:
   - Ya tenemos "tipo_obra" (comedia, auto, zarzuela, etc.)
   - Buscar clasificaciones más específicas si están disponibles

2. TEMAS:
   - Buscar descripciones temáticas en el texto
   - Referencias a temas literarios comunes del Siglo de Oro

3. NOTA:
   - Esta información puede no estar explícita en Fuentes IX
   - Priorizar otras tareas primero
```

---

## 📝 Formato de Salida Estándar

### Estructura JSON para cada archivo procesado

```json
{
  "metadata": {
    "archivo": "FUENTES IX 1_part_001_ALL_PAGES_texto_extraido.txt",
    "fecha_procesamiento": "YYYY-MM-DD",
    "total_obras_identificadas": 0,
    "total_representaciones": 0,
    "total_mecenas": 0,
    "total_lugares": 0
  },
  "obras": [
    {
      "titulo": "Título de la obra",
      "titulo_alternativo": ["Título alternativo"],
      "autor": "Nombre del autor",
      "fecha_creacion_estimada": "Fecha si está disponible",
      "edicion_principe": "Información sobre edición príncipe",
      "manuscritos_conocidos": ["Lista de manuscritos"],
      "mecenas": "Mecenas principal",
      "genero": "Género si está disponible",
      "subgenero": "Subgénero si está disponible",
      "tema": "Tema si está disponible",
      "pagina_pdf": "Número de página",
      "texto_original": "Fragmento del texto",
      "confianza": "alto|medio|bajo"
    }
  ],
  "representaciones": [
    {
      "obra_titulo": "Título de la obra",
      "fecha": "Fecha original",
      "fecha_formateada": "YYYY-MM-DD",
      "compañia": "Nombre de la compañía",
      "director_compañia": "Director",
      "lugar_nombre": "Nombre del lugar",
      "lugar_tipo": "tipo",
      "lugar_region": "Región",
      "lugar_ciudad": "Ciudad",
      "mecenas": "Mecenas si aplica",
      "organizadores_fiesta": ["Lista de organizadores"],
      "personajes_historicos": ["Lista de personajes"],
      "tipo_funcion": "tipo",
      "publico": "tipo de público",
      "observaciones": "Observaciones adicionales",
      "pagina_pdf": "Número de página",
      "texto_original": "Fragmento del texto",
      "confianza": "alto|medio|bajo"
    }
  ],
  "lugares_nuevos": [
    {
      "nombre": "Nombre del lugar",
      "tipo": "tipo_lugar",
      "region": "Región",
      "ciudad": "Ciudad",
      "descripcion": "Descripción",
      "coordenadas": {"lat": null, "lng": null}
    }
  ],
  "mecenas_unicos": [
    {
      "nombre": "Nombre del mecenas",
      "tipo": "rey|reina|noble|organizador|otro",
      "frecuencia": 0,
      "obras_relacionadas": ["Lista de títulos"]
    }
  ]
}
```

---

## 🔄 Proceso de Integración con DB

### Paso 1: Validación y Limpieza
1. Validar formato JSON
2. Verificar campos requeridos
3. Normalizar nombres (lugares, compañías, mecenas)
4. Detectar duplicados

### Paso 2: Matching con Obras Existentes
1. Buscar obras por título (fuzzy matching)
2. Si no existe, crear nueva obra
3. Si existe, actualizar campos faltantes

### Paso 3: Crear/Actualizar Representaciones
1. Verificar si la representación ya existe (obra + fecha + lugar)
2. Si no existe, crear nueva
3. Si existe, actualizar campos faltantes

### Paso 4: Crear/Actualizar Lugares
1. Buscar lugar por nombre y región
2. Si no existe, crear nuevo lugar
3. Usar coordenadas de `geographic_metadata.json` si están disponibles

### Paso 5: Actualizar Mecenas
1. Actualizar campo `mecenas` en Obra si aplica
2. Actualizar campo `mecenas` en Representacion
3. Actualizar campos `organizadores_fiesta` y `personajes_historicos`

---

## 📊 Métricas de Éxito

### Objetivos por Tarea

| Tarea | Objetivo | Métrica |
|-------|----------|---------|
| Mecenas | +500 registros | % obras con mecenas > 25% |
| Lugares | +100 lugares únicos | % representaciones con lugar > 80% |
| Representaciones | +1000 representaciones | Total representaciones > 3000 |
| Compañías | Normalizar todas | % representaciones con compañía > 90% |
| Fechas | +300 fechas de creación | % obras con fecha > 45% |
| Ediciones | +200 ediciones príncipes | % obras con edición > 25% |

---

## ⚠️ Consideraciones Importantes

1. **Confianza de Datos**: Siempre incluir campo `confianza` (alto/medio/bajo)
2. **Discrepancias**: Documentar discrepancias entre fuentes en `observaciones`
3. **Texto Original**: Siempre incluir fragmento del texto original para verificación
4. **Página PDF**: Incluir número de página para trazabilidad
5. **No Inventar**: Si no hay información clara, dejar campo vacío, no inventar datos
6. **Normalización**: Usar nombres normalizados pero conservar originales
7. **Relaciones**: Mantener relaciones obra-representación-lugar-mecenas

---

## 🚀 Orden de Ejecución Recomendado

1. **Fase 1**: Mecenas (Tarea 1) - Archivos part_001 a part_003
2. **Fase 2**: Lugares y Representaciones (Tarea 2) - Archivos part_001 a part_006
3. **Fase 3**: Compañías (Tarea 3) - Todos los archivos
4. **Fase 4**: Fechas (Tarea 4) - Todos los archivos
5. **Fase 5**: Ediciones y Manuscritos (Tarea 5) - Todos los archivos
6. **Fase 6**: Títulos Alternativos (Tarea 6) - Todos los archivos
7. **Fase 7**: Géneros y Temas (Tarea 7) - Si hay tiempo

---

## 📚 Referencias

- Modelos Django: `apps/obras/models.py`, `apps/representaciones/models.py`, `apps/lugares/models.py`
- Metadatos geográficos: `data/fuentesix/geographic_metadata.json`
- Lugares procesados: `data/fuentesix/lugares_procesados.json`
- Estructura de datos: `CAMPOS_COMPLETOS.md`

---

**Última actualización**: 2025-01-27  
**Versión**: 1.0






