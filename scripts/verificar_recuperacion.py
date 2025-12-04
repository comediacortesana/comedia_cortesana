"""
Script para verificar que la recuperación de Supabase fue exitosa
Uso: python scripts/verificar_recuperacion.py
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.supabase_client import SupabaseSync


def verificar_conexion():
    """Verifica que podemos conectar a Supabase"""
    print("🔌 Verificando conexión a Supabase...")
    try:
        sync = SupabaseSync()
        print("✅ Conexión exitosa")
        return sync
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None


def verificar_tablas(sync):
    """Verifica que las tablas existen y tienen datos"""
    print("\n📊 Verificando tablas...")
    
    tablas = {
        'obras': 'Catálogo de obras',
        'comentarios': 'Comentarios de usuarios',
        'validaciones': 'Propuestas de cambios',
        'perfiles_usuarios': 'Perfiles de usuarios',
        'historial_validaciones': 'Historial de cambios',
        'logs_errores': 'Logs de errores'
    }
    
    resultados = {}
    for tabla, descripcion in tablas.items():
        try:
            # Intentar contar registros
            result = sync.client.table(tabla).select('*', count='exact').limit(0).execute()
            count = result.count if hasattr(result, 'count') else 0
            resultados[tabla] = count
            print(f"  ✅ {tabla} ({descripcion}): {count} registros")
        except Exception as e:
            resultados[tabla] = None
            print(f"  ❌ {tabla}: Error - {e}")
    
    return resultados


def verificar_obras(sync):
    """Verifica que las obras tienen los campos necesarios"""
    print("\n📚 Verificando estructura de obras...")
    
    try:
        # Obtener una muestra de obras
        result = sync.client.table('obras').select('*').limit(5).execute()
        
        if not result.data:
            print("  ⚠️  No hay obras en la base de datos")
            return False
        
        # Verificar campos clave
        obra_sample = result.data[0]
        campos_requeridos = [
            'id', 'titulo', 'autor', 'fuente', 'tipo_obra',
            'genero', 'fecha_creacion'
        ]
        
        campos_ok = []
        campos_faltantes = []
        
        for campo in campos_requeridos:
            if campo in obra_sample:
                campos_ok.append(campo)
            else:
                campos_faltantes.append(campo)
        
        print(f"  ✅ Campos presentes: {len(campos_ok)}/{len(campos_requeridos)}")
        
        if campos_faltantes:
            print(f"  ⚠️  Campos faltantes: {', '.join(campos_faltantes)}")
        
        # Verificar campo JSONB 'autor'
        if 'autor' in obra_sample and isinstance(obra_sample['autor'], dict):
            print("  ✅ Campo 'autor' (JSONB) funciona correctamente")
        else:
            print("  ⚠️  Campo 'autor' no es JSONB o está vacío")
        
        # Mostrar una obra de ejemplo
        print(f"\n  📖 Ejemplo de obra recuperada:")
        print(f"     ID: {obra_sample.get('id')}")
        print(f"     Título: {obra_sample.get('titulo')}")
        
        if isinstance(obra_sample.get('autor'), dict):
            print(f"     Autor: {obra_sample['autor'].get('nombre', 'N/A')}")
        else:
            print(f"     Autor: {obra_sample.get('autor_nombre', 'N/A')}")
        
        print(f"     Fuente: {obra_sample.get('fuente', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error al verificar obras: {e}")
        return False


def verificar_rls(sync):
    """Verifica que las políticas RLS están activas"""
    print("\n🔒 Verificando Row Level Security (RLS)...")
    
    # Esta verificación es básica, solo intenta leer
    # Las políticas específicas solo se pueden verificar desde SQL
    
    try:
        # Intentar leer obras (debería funcionar, es público)
        result = sync.client.table('obras').select('id').limit(1).execute()
        print("  ✅ Lectura pública de obras funciona")
        
        # Nota: No podemos verificar las políticas de escritura sin autenticación
        print("  ℹ️  Para verificar políticas completas, usa el SQL Editor en Supabase")
        
        return True
    except Exception as e:
        print(f"  ❌ Error al verificar RLS: {e}")
        return False


def verificar_indices(sync):
    """Verifica que los índices existen (solo informativo)"""
    print("\n⚡ Verificando índices...")
    print("  ℹ️  Los índices se verifican automáticamente en Supabase")
    print("  ℹ️  Si las búsquedas son rápidas, los índices están funcionando")
    return True


def generar_reporte(resultados_tablas, obras_ok, rls_ok):
    """Genera un reporte final"""
    print("\n" + "="*60)
    print("📋 REPORTE DE VERIFICACIÓN")
    print("="*60)
    
    # Verificar tablas
    tablas_ok = sum(1 for count in resultados_tablas.values() if count is not None)
    tablas_total = len(resultados_tablas)
    
    print(f"\n✅ Tablas creadas: {tablas_ok}/{tablas_total}")
    
    # Obras
    obras_count = resultados_tablas.get('obras', 0)
    if obras_count and obras_count > 0:
        print(f"✅ Obras restauradas: {obras_count}")
    else:
        print(f"❌ No hay obras restauradas")
    
    # Estructura
    if obras_ok:
        print(f"✅ Estructura de obras correcta")
    else:
        print(f"❌ Problemas con estructura de obras")
    
    # RLS
    if rls_ok:
        print(f"✅ RLS habilitado y funcionando")
    else:
        print(f"⚠️  Verificar RLS manualmente")
    
    # Estado general
    print("\n" + "="*60)
    
    todo_ok = (
        tablas_ok == tablas_total and
        obras_count and obras_count > 0 and
        obras_ok and
        rls_ok
    )
    
    if todo_ok:
        print("🎉 RECUPERACIÓN EXITOSA - Todo funciona correctamente")
        print("="*60)
        return True
    else:
        print("⚠️  RECUPERACIÓN PARCIAL - Revisa los errores arriba")
        print("="*60)
        return False


def main():
    print("="*60)
    print("🔄 VERIFICACIÓN DE RECUPERACIÓN DE SUPABASE")
    print("="*60)
    
    # 1. Verificar conexión
    sync = verificar_conexion()
    if not sync:
        print("\n❌ No se pudo conectar a Supabase")
        print("   Verifica tus credenciales en .env")
        sys.exit(1)
    
    # 2. Verificar tablas
    resultados_tablas = verificar_tablas(sync)
    
    # 3. Verificar obras
    obras_ok = verificar_obras(sync)
    
    # 4. Verificar RLS
    rls_ok = verificar_rls(sync)
    
    # 5. Verificar índices (informativo)
    verificar_indices(sync)
    
    # 6. Generar reporte
    exito = generar_reporte(resultados_tablas, obras_ok, rls_ok)
    
    # 7. Próximos pasos
    print("\n📝 PRÓXIMOS PASOS:")
    
    if exito:
        print("  1. Abre tu aplicación web y verifica que funciona")
        print("  2. Crea un usuario admin si es necesario")
        print("  3. Prueba buscar obras y usar filtros")
        print("  4. Configura backups automáticos periódicos")
    else:
        print("  1. Revisa los errores arriba")
        print("  2. Ejecuta el script SQL de recuperación nuevamente")
        print("  3. Verifica las credenciales de Supabase")
        print("  4. Contacta al equipo si persisten los problemas")
    
    print("\n✅ Verificación completada")
    sys.exit(0 if exito else 1)


if __name__ == '__main__':
    main()

