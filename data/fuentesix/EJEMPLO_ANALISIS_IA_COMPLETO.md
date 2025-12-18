# 📊 Ejemplo Completo: Análisis de IA para Representación

## Ejemplo Real: "El Pastor Fido" (22 mayo 1687)

### Datos Extraídos (estructurados)
```json
{
  "obra_titulo": "El Pastor Fido",
  "fecha": "22 de mayo de 1687",
  "fecha_formateada": "1687-05-22",
  "compañia": "compañía de Agustín Manuel",
  "lugar_nombre": "Saloncillo del Buen Retiro",
  "confianza": "medio"
}
```

### Análisis de IA (guardado en `analisis_ia_fuentes_ix`)

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
    "Saloncillo y Saloncete son ambas salas del Buen Retiro, probablemente la misma representación",
    "La discrepancia es menor: ambas son variantes del nombre de la misma sala"
  ],
  
  "discrepancias": [
    {
      "tipo": "lugar",
      "descripcion": "Diferencia en nombre de sala",
      "fuente_1": {
        "fuente": "Fuentes I",
        "lugar": "Saloncete",
        "confianza": "medio"
      },
      "fuente_2": {
        "fuente": "Fuentes V",
        "lugar": "Saloncillo del Buen Retiro",
        "confianza": "alto"
      },
      "resolucion_sugerida": "Ambas son salas del Buen Retiro. Usar 'Saloncillo del Buen Retiro' como nombre canónico.",
      "confianza_resolucion": "alto"
    }
  ],
  
  "patrones_detectados": [
    "[FECHA] la compañía de [COMPAÑÍA] representó [OBRA], en [LUGAR], según [FUENTE]",
    "Patrón de discrepancia: misma representación, diferentes nombres de lugar"
  ],
  
  "confianza": "medio",
  "archivo_fuente": "FUENTES IX 1_part_001_ALL_PAGES_texto_extraido.txt",
  "pagina_pdf": 134,
  "linea_texto": 134,
  "fuente_ia": "sistema_extraccion_inteligente",
  "version_ia": "1.0.0",
  "version_datos": "1.0.0",
  "estado": "pendiente_revision"
}
```

---

## Ejemplo: Discrepancia de Fecha y Compañía

### Caso: "El Mariscal de Virón" (octubre 1685)

```json
{
  "tipo": "discrepancia_fuentes",
  "tipo_discrepancia": "fecha_y_compañia",
  "registro_id": "temp_part_001_rep_2",
  
  "fuente_1": {
    "fuente": "Fuentes V",
    "fecha": "3 de octubre de 1685",
    "compañia": "compañía de Rosendo López",
    "lugar": "Palacio"
  },
  
  "fuente_2": {
    "fuente": "Fuentes I",
    "fecha": "4 de octubre de 1685",
    "compañia": "compañía de Manuel de Mosquera",
    "lugar": "Palacio"
  },
  
  "interpretacion": "Es poco probable que dos compañías distintas hubiesen interpretado la misma comedia dos días seguidos. Posiblemente misma representación con datos contradictorios. Sin corroboración de otras fuentes, es imposible determinar cuál es correcta.",
  
  "confianza_resolucion": "medio",
  
  "frases_originales": [
    "Según Fuentes V, la compañía de Rosendo López representó El Mariscal de Virón en Palacio el 3 de octubre de 1685",
    "pero Fuentes I registra una representación de la misma comedia por la compañía de Manuel de Mosquera el día siguiente, 4 de octubre, también en Palacio"
  ],
  
  "contexto_adicional": {
    "nota": "Es posible que las dos compañías se hubiesen combinado para efectuar la representación",
    "ejemplo_similar": "Tal como pasó el 21 de septiembre del mismo año cuando hicieron juntas La profetisa Casandra"
  }
}
```

---

## Ejemplo: Análisis de Patrón Detectado

```json
{
  "tipo": "patron_deteccion",
  "tipo_patron": "representacion",
  "patron": "(1) [FECHA]. [COMPAÑÍA]. [LUGAR] ([FUENTE]);",
  "ejemplos": [
    "(1) 9 de enero de 1681. Jerónimo García. Palacio (Fuentes V);",
    "(2) 23 de enero de 1681. Jerónimo García. Representación palaciega (Fuentes V);",
    "(3) 12 de octubre de 1687. Simón Aguado. Buen Retiro, Saloncete (Fuentes I);"
  ],
  "confianza": "alto",
  "total_ejemplos": 18,
  "fecha_deteccion": "2025-01-27T13:00:00Z"
}
```

---

## Ejemplo: Frase con Contexto Completo

```json
{
  "tipo": "frase_contexto",
  "frase_original": "El 22 de mayo de 1687 la compañía de Agustín Manuel representó El Pastor Fido, en el Saloncillo del Buen Retiro, según Fuentes V, y en el Saloncete, según Fuentes I.",
  
  "terminos_identificados": {
    "fecha": ["22 de mayo de 1687"],
    "compañia": ["compañía de Agustín Manuel", "Agustín Manuel"],
    "obra": ["El Pastor Fido"],
    "lugar": ["Saloncillo del Buen Retiro", "Saloncete"],
    "fuente": ["Fuentes V", "Fuentes I"]
  },
  
  "contexto_anterior": "Los certificados notariales y los documentos palaciegos pueden, por ejemplo, ofrecer evidencia contradictoria en cuanto al lugar de la representación.",
  
  "contexto_posterior": "Puede que las dos fuentes registren fechas al parecer contradictorias.",
  
  "numero_linea": 134,
  "longitud_frase": 145,
  "tokens": 25
}
```

---

## Visualización en Frontend

### Badge de Análisis IA
```
[IA] Análisis automático - Confianza: 🟡 Medio
```

### Expandible con:
- 📝 Frases originales (2)
- 💡 Interpretaciones (3)
- ⚠️ Discrepancias (1)
- 🔍 Patrones detectados (2)

### Botones de Acción:
- ✅ Marcar como revisado
- ✏️ Editar interpretación
- 📌 Integrar datos
- ❌ Rechazar análisis

---

## Ventajas del Sistema

1. **Transparencia Total**: Ver exactamente qué interpretó la IA y por qué
2. **Revisión Controlada**: Poder revisar y corregir antes de integrar
3. **Trazabilidad**: Saber de dónde viene cada dato (frase original)
4. **Aprendizaje Continuo**: Los patrones mejoran con el tiempo
5. **Confianza Graduada**: Priorizar revisión de datos de baja confianza

---

**Última actualización**: 2025-01-27






