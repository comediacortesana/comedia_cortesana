# 📊 Guía: Editar Obras en Google Sheets

## 🎯 Dos Formas de Exportar a CSV

### Opción 1: Desde el HTML (filtrado) ⭐
**Ideal para**: Exportar solo las obras filtradas

1. Abre: `index.html` en tu navegador
2. Aplica filtros (ej: solo Lope de Vega, solo comedias)
3. Click en **"📊 Exportar a CSV"**
4. Se descarga: `teatro_espanol_TIMESTAMP.csv`

**Ventaja**: Solo exportas lo que necesitas editar

### Opción 2: Desde Django (todas) 🚀
**Ideal para**: Exportar todas las 2,100 obras

```bash
# Exportar TODAS las obras
python scripts/export_to_csv.py

# Exportar solo 500
python scripts/export_to_csv.py --max 500

# Incluir textos largos del PDF (archivo más grande)
python scripts/export_to_csv.py --con-textos
```

**Archivo generado**: `filtro_basico/obras_completas.csv`

---

## 📥 Importar a Google Sheets

### Paso 1: Crear Google Sheet nuevo
1. Ve a https://sheets.google.com
2. Click en **"+ Nuevo"** → **"Hoja de cálculo en blanco"**
3. Nómbrala: **"DELIA - Teatro Español - Edición"**

### Paso 2: Importar el CSV
1. **Archivo** → **Importar**
2. **Subir** → Arrastra `obras_completas.csv`
3. **Configuración de importación**:
   - Tipo de separador: **Coma**
   - Detectar automáticamente: ✅
   - Convertir texto a números y fechas: ❌ (IMPORTANTE)
4. Click **"Importar datos"**
5. **Ubicación**: **Reemplazar hoja de cálculo actual**

### Paso 3: Verificar Importación
- ✅ Debería haber 2,101 filas (1 encabezado + 2,100 obras)
- ✅ 32-38 columnas (según lo que exportaste)
- ✅ Los acentos se ven correctamente
- ✅ No hay caracteres raros

---

## 📝 Editar Colaborativamente

### Compartir con Investigadores:
1. Click **"Compartir"** (arriba derecha)
2. Añade emails de investigadores
3. Permisos: **"Editor"** (pueden editar)
4. ✅ Click **"Enviar"**

### Sugerencias de Organización:

#### Congelar Filas y Columnas:
1. Selecciona fila 1 (encabezados)
2. **Ver** → **Inmovilizar** → **1 fila**
3. (Opcional) Inmovilizar columnas ID y Título

#### Añadir Filtros:
1. Selecciona fila de encabezados
2. **Datos** → **Crear un filtro**
3. Ahora puedes filtrar por columna

#### Código de Colores:
```
Regla de formato condicional:
- Si celda está vacía → Color amarillo claro
- Si tiene "Anónimo" → Color naranja
- Si tiene datos → Color verde claro
```

#### Añadir Columna de Estado:
1. Añade columna: **"Estado de Revisión"**
2. Valores posibles:
   - ✅ Completo
   - 🔄 En progreso
   - ⚠️ Necesita revisión
   - ⚪ Pendiente

---

## 🔄 Workflow de Edición Colaborativa

### Fase 1: Asignación
```
Investigador 1: Filas 1-700 (Obras A-G)
Investigador 2: Filas 701-1400 (Obras H-P)
Investigador 3: Filas 1401-2100 (Obras Q-Z)
```

### Fase 2: Priorización
1. Primero completar campos críticos:
   - Género, Subgénero, Tema
   - Fecha de creación
   - Actos y Versos
2. Luego campos secundarios:
   - Manuscritos y ediciones
   - Notas bibliográficas
3. Finalmente campos especializados:
   - Música
   - Mecenazgo

### Fase 3: Validación
1. Revisar campos completados
2. Verificar contra fuentes
3. Marcar como "✅ Completo"

### Fase 4: Exportar
1. **Archivo** → **Descargar** → **CSV**
2. Guardar como: `obras_editadas_FECHA.csv`

---

## 📤 Importar de Vuelta a Django

### Script de Importación (crear):

```python
# scripts/import_from_csv.py
import csv
from apps.obras.models import Obra
from apps.autores.models import Autor

with open('filtro_basico/obras_editadas_2025-10-30.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        try:
            obra = Obra.objects.get(id=row['ID'])
            
            # Actualizar campos editados
            if row['Género']:
                obra.genero = row['Género']
            if row['Subgénero']:
                obra.subgenero = row['Subgénero']
            if row['Tema']:
                obra.tema = row['Tema']
            if row['Fecha de Creación']:
                obra.fecha_creacion_estimada = row['Fecha de Creación']
            if row['Número de Actos']:
                obra.actos = int(row['Número de Actos'])
            if row['Número de Versos']:
                obra.versos = int(row['Número de Versos'])
            
            # ... más campos ...
            
            obra.save()
            print(f"✅ Actualizada: {obra.titulo_limpio}")
            
        except Obra.DoesNotExist:
            print(f"⚠️ Obra ID {row['ID']} no encontrada")
        except Exception as e:
            print(f"❌ Error en fila {row['ID']}: {e}")
```

### Comando:
```bash
python scripts/import_from_csv.py
```

---

## 💡 Tips para Google Sheets

### 1. Validación de Datos
Añade validación a columnas específicas:

**Columna "Tipo de Obra":**
- Datos → Validación de datos
- Criterios: Lista de elementos
- Valores: `comedia,auto,zarzuela,entremes,tragedia,loa,sainete,baile,otro`

**Columna "Música Conservada":**
- Lista: `Sí,No`

**Columna "Fuente":**
- Lista: `FUENTESXI,CATCOM,AMBAS`

### 2. Fórmulas Útiles

**Contar campos vacíos por fila:**
```
=COUNTBLANK(B2:AJ2)
```

**Porcentaje de completitud:**
```
=(32-COUNTBLANK(B2:AJ2))/32*100
```

**Marcar filas incompletas:**
```
=IF(COUNTBLANK(B2:AJ2)>20,"⚠️ Muy incompleta","✅ Aceptable")
```

### 3. Crear Gráficos
- Gráfico de barras: Obras por autor
- Gráfico circular: Tipos de obra
- Gráfico de línea: Obras por década

### 4. Comentarios y Notas
- Click derecho en celda → **"Insertar comentario"**
- Útil para: "Verificar esta fecha", "Fuente dudosa", etc.

---

## 📊 Columnas del CSV (32 campos)

| # | Columna | Editable | Notas |
|---|---------|----------|-------|
| 1 | ID | ❌ No | Clave única |
| 2 | Título | ✅ Sí | Normalizado |
| 3 | Título Original | ✅ Sí | Como aparece en fuente |
| 4 | Títulos Alternativos | ✅ Sí | Separar con ; |
| 5 | Autor | ⚠️ Cuidado | Debe existir en tabla autores |
| 6 | Autor Nombre Completo | ✅ Sí | |
| 7 | Autor Nacimiento | ✅ Sí | Formato libre |
| 8 | Autor Muerte | ✅ Sí | Formato libre |
| 9 | Autor Época | ✅ Sí | Ej: Siglo de Oro |
| 10 | Autor Biografía | ✅ Sí | Texto largo OK |
| 11 | Tipo de Obra | ✅ Sí | Ver lista validación |
| 12 | Género | ✅ Sí | Prioritario ⭐ |
| 13 | Subgénero | ✅ Sí | Prioritario ⭐ |
| 14 | Tema | ✅ Sí | Prioritario ⭐ |
| 15 | Fuente Principal | ⚠️ | FUENTESXI, CATCOM, AMBAS |
| 16 | Origen de Datos | ⚠️ | web, pdf, manual |
| 17 | Página PDF | ✅ Sí | Número |
| 18 | Número de Actos | ✅ Sí | Prioritario ⭐ |
| 19 | Número de Versos | ✅ Sí | |
| 20 | Idioma | ✅ Sí | Default: Español |
| 21 | Fecha de Creación | ✅ Sí | Prioritario ⭐ |
| 22 | Música Conservada | ✅ Sí | Sí/No |
| 23 | Compositor | ✅ Sí | |
| 24 | Bibliotecas con Música | ✅ Sí | |
| 25 | Bibliografía Musical | ✅ Sí | |
| 26 | Mecenas | ✅ Sí | |
| 27 | Edición Príncipe | ✅ Sí | |
| 28 | Notas Bibliográficas | ✅ Sí | |
| 29 | Manuscritos Conocidos | ✅ Sí | |
| 30 | Ediciones Conocidas | ✅ Sí | |
| 31 | Notas | ✅ Sí | |
| 32 | Observaciones | ✅ Sí | |

---

## 🎨 Formato Recomendado en Google Sheets

### Colores por Prioridad:
```
🔴 Rojo: Campos críticos vacíos (Género, Tema, Fecha)
🟡 Amarillo: Campos importantes vacíos (Actos, Versos)
🟢 Verde: Campos completos
⚪ Blanco: Campos opcionales vacíos
```

### Ancho de Columnas:
- ID: 50px
- Título: 200px
- Autor: 150px
- Campos de texto corto: 120px
- Campos de texto largo (biografía, notas): 300px

---

## 🔄 Ciclo de Trabajo

```
Django → CSV → Google Sheets → Edición → CSV → Django
   ↓                                              ↑
Export                                        Import
```

### Timeline:
1. **Día 1**: Exportar CSV → Compartir con investigadores
2. **Días 2-7**: Investigadores completan campos
3. **Día 8**: Descargar CSV editado
4. **Día 8**: Importar de vuelta a Django
5. **Día 8**: Actualizar JSON y GitHub Pages
6. **Repetir** según sea necesario

---

## 📋 Checklist para Investigadores

**Antes de empezar a editar:**
- [ ] CSV importado correctamente
- [ ] Encabezados congelados
- [ ] Filtros activados
- [ ] Formato condicional aplicado
- [ ] Validación de datos configurada

**Durante la edición:**
- [ ] No eliminar la columna ID
- [ ] No cambiar el orden de columnas
- [ ] Usar validación para campos con opciones
- [ ] Añadir comentarios en celdas dudosas
- [ ] Guardar frecuentemente (auto-guardado de Sheets)

**Al terminar:**
- [ ] Revisar que no haya celdas con #ERROR
- [ ] Verificar acentos y caracteres especiales
- [ ] Descargar como CSV (no como Excel)
- [ ] Enviar o compartir con desarrollador

---

## 🚨 Errores Comunes y Soluciones

### Error 1: Acentos mal
**Causa**: Encoding incorrecto  
**Solución**: El CSV usa UTF-8-BOM, Google Sheets lo detecta automáticamente

### Error 2: Comas en el texto rompen columnas
**Causa**: CSV usa coma como separador  
**Solución**: El script escapea automáticamente con comillas

### Error 3: Saltos de línea rompen filas
**Causa**: Saltos de línea en notas/observaciones  
**Solución**: El script envuelve en comillas los campos largos

### Error 4: Al re-importar fallan algunos IDs
**Causa**: IDs modificados o borrados  
**Solución**: ⚠️ NUNCA modificar columna ID

---

## 💾 Comandos Útiles

### Exportar solo obras incompletas:
```python
# Crear script custom
from apps.obras.models import Obra

# Obras sin género o tema
obras = Obra.objects.filter(
    Q(genero='') | Q(tema='')
)

# Exportar solo esas
# ... (usar lógica del export_to_csv.py)
```

### Exportar por fuente:
```bash
# Solo CATCOM
python -c "
from apps.obras.models import Obra
obras = Obra.objects.filter(fuente_principal='CATCOM')
# ... exportar
"
```

### Ver progreso de completitud:
```python
# Estadísticas de campos vacíos
from apps.obras.models import Obra
from django.db.models import Q

total = Obra.objects.count()
sin_genero = Obra.objects.filter(genero='').count()
sin_tema = Obra.objects.filter(tema='').count()
sin_fecha = Obra.objects.filter(fecha_creacion_estimada='').count()

print(f"Sin género: {sin_genero}/{total} ({sin_genero/total*100:.1f}%)")
print(f"Sin tema: {sin_tema}/{total} ({sin_tema/total*100:.1f}%)")
print(f"Sin fecha: {sin_fecha}/{total} ({sin_fecha/total*100:.1f}%)")
```

---

## 🎯 Campos Prioritarios para Completar

Según la investigación teatral, estos son los más importantes:

### 🔴 Prioridad ALTA (para clasificación):
- Género
- Subgénero
- Tema
- Fecha de creación
- Número de actos

### 🟡 Prioridad MEDIA (para análisis):
- Número de versos
- Manuscritos conocidos
- Ediciones conocidas
- Edición príncipe

### 🟢 Prioridad BAJA (complementarios):
- Compositor
- Bibliotecas de música
- Bibliografía musical

---

## 📤 Re-importar a Django

### Opción 1: Script Automático (crear)

```bash
# Crear script: scripts/import_from_csv.py
python scripts/import_from_csv.py filtro_basico/obras_editadas.csv
```

### Opción 2: Manualmente en Django Shell

```python
python manage.py shell

import csv
from apps.obras.models import Obra

with open('filtro_basico/obras_editadas.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    actualizadas = 0
    
    for row in reader:
        try:
            obra = Obra.objects.get(id=row['ID'])
            
            # Actualizar solo si hay datos nuevos
            if row['Género'] and not obra.genero:
                obra.genero = row['Género']
            if row['Tema'] and not obra.tema:
                obra.tema = row['Tema']
            if row['Fecha de Creación'] and not obra.fecha_creacion_estimada:
                obra.fecha_creacion_estimada = row['Fecha de Creación']
            
            obra.save()
            actualizadas += 1
            
            if actualizadas % 100 == 0:
                print(f"✅ {actualizadas} obras actualizadas...")
                
        except Exception as e:
            print(f"❌ Error en ID {row['ID']}: {e}")
    
    print(f"\n🎉 Total actualizadas: {actualizadas}")
```

### Opción 3: Desde Admin de Django
1. Panel admin → Obras
2. Importar/Exportar (si tienes django-import-export)
3. Cargar CSV
4. Preview de cambios
5. Confirmar importación

---

## 📊 Estructura del CSV

### Ejemplo de fila:

```csv
ID,Título,Autor,Tipo de Obra,Género,Tema,Actos,Fecha de Creación
3058,A Dios por razon de estado,Anónimo,comedia,Religiosa,Devoción,3,1650
```

### Después de editar en Sheets:

```csv
ID,Título,Autor,Tipo de Obra,Género,Tema,Actos,Fecha de Creación
3058,A Dios por razon de estado,Anónimo,comedia,Religiosa,Devoción y razón de estado,3,1650-1660
```

---

## ✅ Ventajas de CSV + Google Sheets

| Ventaja | Descripción |
|---------|-------------|
| ✅ **Colaborativo** | Múltiples investigadores a la vez |
| ✅ **Historial** | Google guarda todas las versiones |
| ✅ **Comentarios** | Discutir cambios en celdas específicas |
| ✅ **Filtros** | Filtrar por tipo, autor, estado |
| ✅ **Fórmulas** | Cálculos automáticos |
| ✅ **Validación** | Evita errores de entrada |
| ✅ **Acceso** | Desde cualquier lugar, cualquier dispositivo |
| ✅ **Gratis** | 100% gratuito con cuenta Google |
| ✅ **Familiar** | Todos saben usar Sheets |

---

## 🎨 Plantilla de Google Sheets (Recomendada)

### Pestañas Sugeridas:

1. **📋 Obras Completas** (CSV importado)
2. **🔴 Pendientes** (filtro: campos vacíos)
3. **✅ Completadas** (filtro: todo lleno)
4. **📊 Estadísticas** (gráficos y métricas)
5. **📝 Instrucciones** (guía para editores)

### Ejemplo de Pestaña "Estadísticas":
```
Total de obras: 2,100
Obras completas: 234 (11%)
Obras en progreso: 876 (42%)
Obras pendientes: 990 (47%)

Por investigador:
- María: 234 obras revisadas
- Juan: 187 obras revisadas
- Ana: 156 obras revisadas
```

---

## 🔐 Permisos Recomendados

### Para Investigadores:
- **Editor**: Pueden editar y comentar

### Para Supervisores:
- **Editor**: Pueden editar y aprobar cambios

### Para Lectura:
- **Lector**: Solo ver (para estudiantes o colaboradores externos)

---

## 📅 Timeline Sugerido

| Semana | Actividad |
|--------|-----------|
| Semana 1 | Exportar CSV → Compartir con equipo |
| Semana 2-4 | Edición colaborativa (campos prioritarios) |
| Semana 5 | Revisión y validación |
| Semana 6 | Re-importar a Django → Actualizar GitHub Pages |
| Semana 7+ | Seguir con campos secundarios |

---

## 🎉 Resultado Final

Después del proceso:
1. ✅ Base de datos Django actualizada
2. ✅ JSON actualizado (`datos_obras.json`)
3. ✅ GitHub Pages con datos completos
4. ✅ Investigadores ven mejoras en tiempo real
5. ✅ Sistema más rico y útil

---

## 📞 Recursos

- **Google Sheets**: https://sheets.google.com
- **Tutorial validación**: https://support.google.com/docs/answer/186103
- **Funciones de Sheets**: https://support.google.com/docs/table/25273
- **Compartir y colaborar**: https://support.google.com/docs/answer/2494822

---

## 💡 Próximo Nivel

### Integración con API de Google Sheets:
```python
# Sincronización bidireccional
# Django ↔ Google Sheets en tiempo real
# Usando Google Sheets API

# Los investigadores editan en Sheets
# Django se actualiza automáticamente cada hora
```

Pero empiezas con el CSV simple que ya funciona perfectamente! 🎭


