# 📊 Sistema de Versionado y Trazabilidad de Datos

## Objetivo

Implementar un sistema que permita:
1. **Trazabilidad completa**: Saber exactamente cuándo se añadieron/modificaron datos
2. **Rollback**: Poder revertir a un estado anterior si hay errores
3. **Validación**: Comparar datos nuevos vs existentes antes de integrar
4. **Auditoría**: Historial completo de cambios en la base de datos

---

## Estructura de Versionado

### 1. Metadatos de Extracción

Cada archivo procesado debe incluir:

```json
{
  "metadata": {
    "archivo_fuente": "FUENTES IX 1_part_001_ALL_PAGES_texto_extraido.txt",
    "fecha_extraccion": "2025-01-27T10:30:00Z",
    "version_extraccion": "1.0.0",
    "metodo_extraccion": "IA_manual",
    "modelo_ia": "gpt-4" (si aplica),
    "confianza_promedio": "alto|medio|bajo",
    "total_registros": 0,
    "checksum": "hash_del_contenido_original"
  }
}
```

### 2. Metadatos por Registro

Cada registro extraído debe incluir:

```json
{
  "datos": {
    // ... datos del registro ...
  },
  "metadata_registro": {
    "fecha_extraccion": "2025-01-27T10:30:00Z",
    "version_extraccion": "1.0.0",
    "archivo_fuente": "part_001",
    "pagina_pdf": 134,
    "texto_original": "fragmento del texto",
    "confianza": "alto|medio|bajo",
    "extractor": "IA|manual",
    "validado": false,
    "fecha_validacion": null,
    "validado_por": null
  }
}
```

### 3. Log de Integración a DB

Cada vez que se integren datos a la DB, crear registro:

```json
{
  "log_integracion": {
    "fecha_integracion": "2025-01-27T15:00:00Z",
    "version_datos": "1.0.0",
    "archivos_procesados": ["part_001", "part_002"],
    "total_registros_nuevos": 0,
    "total_registros_actualizados": 0,
    "total_registros_omitidos": 0,
    "errores": [],
    "advertencias": [],
    "usuario": "nombre_usuario",
    "commit_hash": "git_commit_hash" (si aplica)
  }
}
```

---

## Sistema de Versiones

### Formato de Versión: `MAJOR.MINOR.PATCH`

- **MAJOR**: Cambios incompatibles (nueva estructura de datos)
- **MINOR**: Nuevas funcionalidades (nuevos campos)
- **PATCH**: Correcciones y mejoras menores

### Ejemplo de Evolución:
- `1.0.0` - Primera extracción (part_001)
- `1.1.0` - Añadido campo "validado_por" 
- `1.2.0` - Añadido campo "checksum"
- `2.0.0` - Cambio en estructura de lugares

---

## Tabla de Auditoría en DB

### Crear tabla `auditoria_datos_fuentes_ix`

```sql
CREATE TABLE IF NOT EXISTS auditoria_datos_fuentes_ix (
    id SERIAL PRIMARY KEY,
    tipo_operacion VARCHAR(50) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    tabla_afectada VARCHAR(100) NOT NULL, -- 'obras', 'representaciones', 'lugares'
    registro_id INTEGER NOT NULL,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    fecha_operacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version_datos VARCHAR(20),
    archivo_fuente VARCHAR(200),
    usuario VARCHAR(100),
    motivo VARCHAR(500),
    confianza VARCHAR(20),
    validado BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_auditoria_fecha ON auditoria_datos_fuentes_ix(fecha_operacion);
CREATE INDEX idx_auditoria_tabla ON auditoria_datos_fuentes_ix(tabla_afectada);
CREATE INDEX idx_auditoria_registro ON auditoria_datos_fuentes_ix(tabla_afectada, registro_id);
```

---

## Proceso de Integración con Versionado

### Paso 1: Preparación
```python
# Generar versión única para esta integración
version = f"1.0.0-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
# Ejemplo: "1.0.0-20250127-153000"
```

### Paso 2: Validación Pre-Integración
```python
# Comparar datos nuevos vs existentes
# Generar reporte de diferencias
# Marcar registros con conflictos
```

### Paso 3: Integración con Logging
```python
# Por cada registro:
# 1. Guardar estado anterior (si existe)
# 2. Aplicar cambios
# 3. Registrar en auditoría
# 4. Añadir metadatos de versión
```

### Paso 4: Generar Reporte
```python
# Reporte de integración con:
# - Total insertados
# - Total actualizados
# - Total omitidos (conflictos)
# - Errores
# - Advertencias
```

---

## Script de Integración con Versionado

### Estructura del Script

```python
class IntegradorDatosFuentesIX:
    def __init__(self, version_datos):
        self.version_datos = version_datos
        self.fecha_integracion = datetime.now()
        self.log_operaciones = []
        
    def integrar_registro(self, tabla, datos_nuevos, registro_existente=None):
        """Integra un registro con logging completo"""
        operacion = {
            'tipo': 'INSERT' if not registro_existente else 'UPDATE',
            'tabla': tabla,
            'datos_anteriores': registro_existente,
            'datos_nuevos': datos_nuevos,
            'version': self.version_datos,
            'fecha': self.fecha_integracion
        }
        
        # Guardar en auditoría ANTES de modificar
        self._guardar_auditoria(operacion)
        
        # Aplicar cambios
        if registro_existente:
            self._actualizar_registro(tabla, datos_nuevos)
        else:
            self._insertar_registro(tabla, datos_nuevos)
            
        self.log_operaciones.append(operacion)
        
    def generar_reporte(self):
        """Genera reporte completo de la integración"""
        return {
            'version': self.version_datos,
            'fecha': self.fecha_integracion.isoformat(),
            'total_operaciones': len(self.log_operaciones),
            'insertados': sum(1 for op in self.log_operaciones if op['tipo'] == 'INSERT'),
            'actualizados': sum(1 for op in self.log_operaciones if op['tipo'] == 'UPDATE'),
            'errores': self.errores,
            'advertencias': self.advertencias
        }
```

---

## Campos de Versión en Modelos Django

### Añadir a modelos existentes:

```python
# En apps/obras/models.py
class Obra(models.Model):
    # ... campos existentes ...
    
    # Campos de versionado
    fecha_importacion_fuentes_ix = models.DateTimeField(null=True, blank=True)
    version_importacion_fuentes_ix = models.CharField(max_length=50, blank=True)
    archivo_fuente_fuentes_ix = models.CharField(max_length=200, blank=True)
    confianza_datos_fuentes_ix = models.CharField(
        max_length=20, 
        choices=[('alto', 'Alto'), ('medio', 'Medio'), ('bajo', 'Bajo')],
        blank=True
    )
    validado_fuentes_ix = models.BooleanField(default=False)
    fecha_validacion_fuentes_ix = models.DateTimeField(null=True, blank=True)
    validado_por_fuentes_ix = models.ForeignKey(
        'usuarios.Usuario',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='obras_validadas_fuentes_ix'
    )
```

---

## Sistema de Snapshots

### Crear snapshots periódicos de la DB

```python
# Script para crear snapshot
def crear_snapshot_db(version, descripcion):
    """Crea un snapshot completo de la DB para una versión específica"""
    snapshot = {
        'version': version,
        'fecha': datetime.now().isoformat(),
        'descripcion': descripcion,
        'obras': exportar_obras(),
        'representaciones': exportar_representaciones(),
        'lugares': exportar_lugares(),
        'checksum': calcular_checksum()
    }
    # Guardar en archivo JSON o tabla especial
    return snapshot
```

---

## Validación Pre-Integración

### Comparar datos nuevos vs existentes

```python
def validar_datos_nuevos(datos_nuevos, datos_existentes):
    """Compara y valida datos nuevos antes de integrar"""
    diferencias = {
        'campos_nuevos': [],  # Campos que no existen en DB actual
        'valores_diferentes': [],  # Campos con valores diferentes
        'conflictos': [],  # Conflictos que requieren decisión manual
        'advertencias': []  # Advertencias menores
    }
    
    for campo, valor_nuevo in datos_nuevos.items():
        valor_existente = datos_existentes.get(campo)
        
        if valor_existente is None:
            diferencias['campos_nuevos'].append(campo)
        elif valor_existente != valor_nuevo:
            diferencias['valores_diferentes'].append({
                'campo': campo,
                'anterior': valor_existente,
                'nuevo': valor_nuevo
            })
            
    return diferencias
```

---

## Formato de Archivo de Extracción con Versionado

```json
{
  "metadata": {
    "archivo_fuente": "FUENTES IX 1_part_001_ALL_PAGES_texto_extraido.txt",
    "fecha_extraccion": "2025-01-27T10:30:00Z",
    "version_extraccion": "1.0.0",
    "metodo_extraccion": "IA_manual",
    "modelo_ia": "gpt-4",
    "confianza_promedio": "alto",
    "total_registros": 18,
    "checksum": "sha256_hash_del_contenido",
    "estado": "pendiente_integracion" // pendiente_integracion | integrado | validado | rechazado
  },
  "obras": [
    {
      "datos": {
        "titulo": "...",
        // ... campos de la obra ...
      },
      "metadata_registro": {
        "fecha_extraccion": "2025-01-27T10:30:00Z",
        "version_extraccion": "1.0.0",
        "archivo_fuente": "part_001",
        "pagina_pdf": 134,
        "texto_original": "...",
        "confianza": "alto",
        "extractor": "IA",
        "validado": false,
        "fecha_validacion": null,
        "validado_por": null,
        "id_temporal": "temp_001_obra_1" // ID temporal antes de integrar
      }
    }
  ],
  "representaciones": [
    // ... mismo formato ...
  ],
  "log_validacion": {
    "fecha_validacion": null,
    "validado_por": null,
    "errores_encontrados": [],
    "advertencias": [],
    "estado": "pendiente"
  }
}
```

---

## Comandos Útiles

### Ver historial de cambios
```sql
SELECT * FROM auditoria_datos_fuentes_ix 
WHERE tabla_afectada = 'obras' 
ORDER BY fecha_operacion DESC;
```

### Ver cambios de una versión específica
```sql
SELECT * FROM auditoria_datos_fuentes_ix 
WHERE version_datos = '1.0.0';
```

### Revertir a una versión anterior
```python
def revertir_a_version(version_objetivo):
    """Reverte todos los cambios de versiones posteriores a la versión objetivo"""
    # 1. Obtener todos los cambios desde version_objetivo
    # 2. Aplicar reversiones en orden inverso
    # 3. Registrar reversión en auditoría
```

---

## Checklist Pre-Integración

Antes de integrar datos a la DB:

- [ ] ✅ Datos extraídos y validados
- [ ] ✅ Versión asignada
- [ ] ✅ Checksum calculado
- [ ] ✅ Comparación con datos existentes realizada
- [ ] ✅ Conflictos identificados y resueltos
- [ ] ✅ Snapshot de DB actual creado
- [ ] ✅ Backup de DB realizado
- [ ] ✅ Script de integración probado en entorno de prueba
- [ ] ✅ Reporte de diferencias generado
- [ ] ✅ Aprobación de integración obtenida

---

## Ejemplo de Uso Completo

```python
# 1. Cargar datos extraídos
datos = cargar_json('extraccion_part_001.json')

# 2. Crear integrador con versión
version = f"1.0.0-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
integrador = IntegradorDatosFuentesIX(version)

# 3. Validar antes de integrar
for obra in datos['obras']:
    obra_existente = buscar_obra_por_titulo(obra['datos']['titulo'])
    diferencias = validar_datos_nuevos(obra['datos'], obra_existente)
    
    if diferencias['conflictos']:
        # Requiere revisión manual
        marcar_para_revision(obra, diferencias)
    else:
        # Integrar automáticamente
        integrador.integrar_registro('obras', obra['datos'], obra_existente)

# 4. Generar reporte
reporte = integrador.generar_reporte()
guardar_reporte(reporte, f"reporte_integracion_{version}.json")

# 5. Crear snapshot
snapshot = crear_snapshot_db(version, f"Integración datos part_001")
```

---

**Última actualización**: 2025-01-27






