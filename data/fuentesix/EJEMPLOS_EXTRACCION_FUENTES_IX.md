# 📖 Ejemplos Concretos de Extracción - Fuentes IX

Este documento contiene ejemplos reales del texto de Fuentes IX para guiar la extracción con IA.

---

## 🎭 Ejemplo 1: Representación con Mecenas y Lugar

### Texto Original (Página 135)
```
En 1684 nos encontramos con otro problema parecido, cuando Fuentes I ofrece evidencia incierta sobre la representación por la compañía de Manuel Vallejo y otra sin especificar de Las armas de la hermosura el 23 de julio, y de El maestro de danzar el día 26, datos que están en conflicto con los de Fuentes V, según los cuales las compañías de Manuel de Vallejo y Manuel de Mosquera representaron juntos El mérito es la corona el día 26 para celebrar el santo de la Reina Madre.
```

### Extracción Esperada

```json
{
  "representaciones": [
    {
      "obra_titulo": "El mérito es la corona",
      "fecha": "26 de julio de 1684",
      "fecha_formateada": "1684-07-26",
      "compañia": "compañía de Manuel de Vallejo y compañía de Manuel de Mosquera",
      "director_compañia": "",
      "lugar_nombre": "Palacio",
      "lugar_tipo": "palacio",
      "lugar_region": "Comunidad de Madrid",
      "lugar_ciudad": "Madrid",
      "mecenas": "Reina Madre",
      "organizadores_fiesta": [],
      "personajes_historicos": ["Reina Madre"],
      "tipo_funcion": "celebración",
      "publico": "corte",
      "observaciones": "Para celebrar el santo de la Reina Madre. Fuentes I menciona otras obras para fechas similares.",
      "pagina_pdf": 135,
      "texto_original": "las compañías de Manuel de Vallejo y Manuel de Mosquera representaron juntos El mérito es la corona el día 26 para celebrar el santo de la Reina Madre",
      "confianza": "alto"
    }
  ]
}
```

---

## 🎭 Ejemplo 2: Representación Palaciega con Lugar Específico

### Texto Original (Página 134)
```
El 22 de mayo de 1687 la compañía de Agustín Manuel representó El Pastor Fido, en el Saloncillo del Buen Retiro, según Fuentes V, y en el Saloncete, según Fuentes I.
```

### Extracción Esperada

```json
{
  "representaciones": [
    {
      "obra_titulo": "El Pastor Fido",
      "fecha": "22 de mayo de 1687",
      "fecha_formateada": "1687-05-22",
      "compañia": "compañía de Agustín Manuel",
      "director_compañia": "Agustín Manuel",
      "lugar_nombre": "Saloncillo del Buen Retiro",
      "lugar_tipo": "palacio",
      "lugar_region": "Comunidad de Madrid",
      "lugar_ciudad": "Madrid",
      "mecenas": "",
      "organizadores_fiesta": [],
      "personajes_historicos": [],
      "tipo_funcion": "representación_normal",
      "publico": "corte",
      "observaciones": "Discrepancia: Fuentes V menciona Saloncillo, Fuentes I menciona Saloncete. Ambas son salas del Buen Retiro.",
      "pagina_pdf": 134,
      "texto_original": "la compañía de Agustín Manuel representó El Pastor Fido, en el Saloncillo del Buen Retiro, según Fuentes V, y en el Saloncete, según Fuentes I",
      "confianza": "medio"
    }
  ]
}
```

---

## 🎭 Ejemplo 3: Representación con Múltiples Mecenas y Motivo

### Texto Original (Página 135)
```
En 1685 cuando hicieron juntas La profetisa Casandra, pero ésta fue una obra de espectáculo, proyectada para festejar el cumpleaños de la Reina María Luisa de Borbón (Fuentes V, pág. 187)
```

### Extracción Esperada

```json
{
  "obras": [
    {
      "titulo": "La profetisa Casandra",
      "mecenas": "María Luisa de Borbón",
      "pagina_pdf": 135,
      "texto_original": "proyectada para festejar el cumpleaños de la Reina María Luisa de Borbón",
      "confianza": "alto"
    }
  ],
  "representaciones": [
    {
      "obra_titulo": "La profetisa Casandra",
      "fecha": "21 de septiembre de 1685",
      "fecha_formateada": "1685-09-21",
      "compañia": "compañías combinadas",
      "lugar_nombre": "Palacio",
      "lugar_tipo": "palacio",
      "mecenas": "María Luisa de Borbón",
      "organizadores_fiesta": [],
      "personajes_historicos": ["María Luisa de Borbón", "Reina"],
      "tipo_funcion": "fiesta",
      "publico": "corte",
      "observaciones": "Obra de espectáculo para festejar cumpleaños de la Reina. Representada por compañías combinadas.",
      "pagina_pdf": 135,
      "texto_original": "proyectada para festejar el cumpleaños de la Reina María Luisa de Borbón",
      "confianza": "alto"
    }
  ]
}
```

---

## 🎭 Ejemplo 4: Títulos Alternativos

### Texto Original (Página 139)
```
Los títulos alternativos dados a las comedias son otra fuente de confusiones. No es difícil identificar Psiquis y Cupido, representada el 3 de diciembre de 1679 por las compañías de Manuel Vallejo y José de Prado, según Fuentes I, con Ni amor se libra de amor, hecha por las mismas compañías el mismo día, según Fuentes V.
```

### Extracción Esperada

```json
{
  "obras": [
    {
      "titulo": "Psiquis y Cupido",
      "titulo_alternativo": ["Ni amor se libra de amor"],
      "pagina_pdf": 139,
      "texto_original": "Psiquis y Cupido... con Ni amor se libra de amor",
      "confianza": "alto"
    }
  ],
  "representaciones": [
    {
      "obra_titulo": "Psiquis y Cupido",
      "fecha": "3 de diciembre de 1679",
      "fecha_formateada": "1679-12-03",
      "compañia": "compañía de Manuel Vallejo y compañía de José de Prado",
      "observaciones": "También conocida como 'Ni amor se libra de amor'",
      "pagina_pdf": 139,
      "confianza": "alto"
    }
  ]
}
```

---

## 🎭 Ejemplo 5: Representación con Discrepancia de Fecha

### Texto Original (Página 134)
```
Según Fuentes V, la compañía de Rosendo López representó El Mariscal de Virón en Palacio el 3 de octubre de 1685, pero Fuentes I registra una representación de la misma comedia por la compañía de Manuel de Mosquera el día siguiente, 4 de octubre, también en Palacio.
```

### Extracción Esperada

```json
{
  "representaciones": [
    {
      "obra_titulo": "El Mariscal de Virón",
      "fecha": "3 de octubre de 1685",
      "fecha_formateada": "1685-10-03",
      "compañia": "compañía de Rosendo López",
      "director_compañia": "Rosendo López",
      "lugar_nombre": "Palacio",
      "lugar_tipo": "palacio",
      "observaciones": "DISCREPANCIA: Fuentes V dice 3 de octubre con compañía de Rosendo López. Fuentes I dice 4 de octubre con compañía de Manuel de Mosquera. Posiblemente misma representación con datos contradictorios.",
      "pagina_pdf": 134,
      "texto_original": "la compañía de Rosendo López representó El Mariscal de Virón en Palacio el 3 de octubre de 1685",
      "confianza": "medio"
    },
    {
      "obra_titulo": "El Mariscal de Virón",
      "fecha": "4 de octubre de 1685",
      "fecha_formateada": "1685-10-04",
      "compañia": "compañía de Manuel de Mosquera",
      "director_compañia": "Manuel de Mosquera",
      "lugar_nombre": "Palacio",
      "lugar_tipo": "palacio",
      "observaciones": "DISCREPANCIA: Fuentes I menciona esta fecha y compañía. Puede ser la misma representación que Fuentes V fecha el 3 de octubre.",
      "pagina_pdf": 134,
      "texto_original": "Fuentes I registra una representación de la misma comedia por la compañía de Manuel de Mosquera el día siguiente, 4 de octubre",
      "confianza": "medio"
    }
  ]
}
```

---

## 🎭 Ejemplo 6: Representación con Lugar Específico del Palacio

### Texto Original (Página 135)
```
En 1695 Fuentes VI ofrece datos sobre la representación el 14 de febrero de El monstruo de los jardines en el Cuarto del Rey y de Cuando no se aguarda en el de la Reina, ambas por la compañía de Damián Polope, y el certificado del escribano dice que «bi entrar dicha compañia en el Salon a las tres y media poco mas o menos para representar dichas comedias».
```

### Extracción Esperada

```json
{
  "representaciones": [
    {
      "obra_titulo": "El monstruo de los jardines",
      "fecha": "14 de febrero de 1695",
      "fecha_formateada": "1695-02-14",
      "compañia": "compañía de Damián Polope",
      "director_compañia": "Damián Polope",
      "lugar_nombre": "Cuarto del Rey",
      "lugar_tipo": "palacio",
      "lugar_region": "Comunidad de Madrid",
      "lugar_ciudad": "Madrid",
      "observaciones": "Representación en el Cuarto del Rey. El certificado menciona que la compañía entró en el Salón a las tres y media.",
      "pagina_pdf": 135,
      "texto_original": "la representación el 14 de febrero de El monstruo de los jardines en el Cuarto del Rey",
      "confianza": "alto"
    },
    {
      "obra_titulo": "Cuando no se aguarda",
      "fecha": "14 de febrero de 1695",
      "fecha_formateada": "1695-02-14",
      "compañia": "compañía de Damián Polope",
      "director_compañia": "Damián Polope",
      "lugar_nombre": "Cuarto de la Reina",
      "lugar_tipo": "palacio",
      "lugar_region": "Comunidad de Madrid",
      "lugar_ciudad": "Madrid",
      "observaciones": "Misma compañía representó dos obras el mismo día en diferentes lugares del palacio.",
      "pagina_pdf": 135,
      "texto_original": "de Cuando no se aguarda en el de la Reina",
      "confianza": "alto"
    }
  ]
}
```

---

## 🎭 Ejemplo 7: Menciones a Organizadores y Gestores

### Texto Original (Página 125)
```
En 1686 el Conde de Monterrey comenta las dificultades causadas por los pagos tardíos, indicando que causa da confusión de no saber yo los días en que se representaron y por que compañías
```

### Extracción Esperada

```json
{
  "personajes_historicos": [
    {
      "nombre": "Conde de Monterrey",
      "tipo": "noble",
      "rol": "gestor_administrativo",
      "contexto": "Mencionado en relación con pagos de representaciones palaciegas",
      "pagina_pdf": 125,
      "texto_original": "el Conde de Monterrey comenta las dificultades causadas por los pagos tardíos",
      "confianza": "alto"
    }
  ]
}
```

---

## 🎭 Ejemplo 8: Referencias a Ediciones y Manuscritos

### Texto Original (Página 139)
```
En este caso, la evidencia del manuscrito 14.940 de la Biblioteca Nacional confirma sin lugar a dudas que se trata de la obra de Pablo Polope y Valdés
```

### Extracción Esperada

```json
{
  "obras": [
    {
      "titulo": "Los tres mayores imperios",
      "autor": "Pablo Polope y Valdés",
      "manuscritos_conocidos": [
        {
          "biblioteca": "Biblioteca Nacional de Madrid",
          "signatura": "14.940",
          "descripcion": "Manuscrito que confirma autoría"
        }
      ],
      "pagina_pdf": 139,
      "texto_original": "la evidencia del manuscrito 14.940 de la Biblioteca Nacional confirma sin lugar a dudas que se trata de la obra de Pablo Polope y Valdés",
      "confianza": "alto"
    }
  ]
}
```

---

## 🎭 Ejemplo 9: Referencias a Ediciones Príncipes

### Texto Original (Página 191)
```
Nos referimos a la edición príncipe solamente. No damos ediciones posteriores, salvo en aquellas ocasiones en que ofrecen datos de importancia para la fecha o paternidad literaria de la obra
```

### Nota para IA
Este texto explica la metodología del libro, pero no contiene datos específicos. Buscar en otras partes del texto referencias concretas a ediciones príncipes.

---

## 🎭 Ejemplo 10: Referencias a "Comedia Nueva"

### Texto Original (Página 147)
```
Quizá por esta razón el convenio entre el Interventor de los teatros y el autor de comedias Manuel de Villaflor, en 1706, obliga a éste a representar nuevas comedias, «las quales han de ser de las que no se hubieren hecho ni representado en esta Corte diez años a esta parte»
```

### Extracción Esperada

```json
{
  "personajes_historicos": [
    {
      "nombre": "Manuel de Villaflor",
      "tipo": "autor_comedias",
      "contexto": "Autor de comedias con convenio en 1706 para representar comedias nuevas",
      "pagina_pdf": 147,
      "confianza": "alto"
    }
  ],
  "notas_contextuales": [
    {
      "concepto": "comedia nueva",
      "definicion": "Comedias que no se hubieren hecho ni representado en esta Corte diez años a esta parte (desde 1696)",
      "año_referencia": 1706,
      "pagina_pdf": 147
    }
  ]
}
```

---

## 📋 Checklist de Validación

Antes de considerar una extracción completa, verificar:

- [ ] ¿Se identificó la obra (título)?
- [ ] ¿Se extrajo la fecha (aunque sea aproximada)?
- [ ] ¿Se identificó el lugar o tipo de lugar?
- [ ] ¿Se identificó la compañía o director?
- [ ] ¿Se incluyó el texto original?
- [ ] ¿Se incluyó el número de página?
- [ ] ¿Se marcó el nivel de confianza?
- [ ] ¿Se documentaron discrepancias si las hay?
- [ ] ¿Se normalizaron nombres (lugares, compañías)?
- [ ] ¿Se relacionaron títulos alternativos si los hay?

---

## 🔍 Patrones Comunes a Buscar

### Patrones de Fecha
- `el [día] de [mes] de [año]`
- `[mes] de [año]`
- `en [año]`
- `durante [año]`
- `antes de [fecha]`
- `después de [fecha]`

### Patrones de Compañía
- `compañía de [nombre]`
- `compañías de [nombre] y [nombre]`
- `la compañía de [nombre]`
- `[nombre] representó`
- `[nombre] hizo`

### Patrones de Lugar
- `en [lugar]`
- `en el [lugar]`
- `en la [lugar]`
- `[lugar], según [fuente]`

### Patrones de Mecenas
- `para [verbo] el [evento] de [persona]`
- `festejar el [evento] de [persona]`
- `celebrar el [evento] de [persona]`
- `en honor de [persona]`
- `por orden de [persona]`
- `mandó [persona]`

### Patrones de Título Alternativo
- `también conocida como`
- `también llamada`
- `título alternativo`
- `= [otro título]` (en contexto de identificación)

---

**Última actualización**: 2025-01-27






