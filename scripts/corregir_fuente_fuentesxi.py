#!/usr/bin/env python3
"""
Script para corregir el valor "FUENTESXI" a "Fuentes IX" 
en el JSON local y en Supabase
"""

import json
import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.supabase_client import get_supabase_client

# Valores a cambiar
VALOR_VIEJO = "FUENTESXI"
VALOR_NUEVO = "Fuentes IX"

def actualizar_json(json_path: Path, dry_run: bool = False):
    """Actualiza el JSON local"""
    print(f"\n{'='*60}")
    print("📄 ACTUALIZANDO JSON LOCAL")
    print(f"{'='*60}")
    
    # Cargar JSON
    print(f"📂 Cargando {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Contar ocurrencias antes
    obras = data.get('obras', []) if isinstance(data, dict) else data
    if not isinstance(obras, list):
        print("❌ Error: El JSON no tiene el formato esperado")
        return 0
    
    contador_antes = 0
    obras_afectadas = []
    
    # Buscar y contar ocurrencias
    for i, obra in enumerate(obras):
        # Buscar en diferentes campos posibles
        campos_fuente = ['fuente', 'Fuente Principal', 'Fuente', 'FUENTE']
        
        for campo in campos_fuente:
            if campo in obra and obra[campo] == VALOR_VIEJO:
                contador_antes += 1
                obras_afectadas.append({
                    'indice': i,
                    'id': obra.get('id') or obra.get('ID') or obra.get('Id'),
                    'titulo': obra.get('titulo') or obra.get('Título') or obra.get('T?tulo', 'Sin título'),
                    'campo': campo
                })
                break  # Solo contar una vez por obra
    
    print(f"🔍 Encontradas {contador_antes} ocurrencias de '{VALOR_VIEJO}'")
    
    if contador_antes == 0:
        print("✅ No hay ocurrencias para corregir")
        return 0
    
    # Mostrar algunas obras afectadas
    print(f"\n📋 Primeras obras afectadas:")
    for obra_info in obras_afectadas[:10]:
        print(f"  - ID: {obra_info['id']}, Título: {obra_info['titulo'][:50]}...")
    if len(obras_afectadas) > 10:
        print(f"  ... y {len(obras_afectadas) - 10} más")
    
    if dry_run:
        print("\n🔍 DRY RUN: No se realizarán cambios")
        return contador_antes
    
    # Realizar cambios
    print(f"\n🔄 Reemplazando '{VALOR_VIEJO}' por '{VALOR_NUEVO}'...")
    contador_cambios = 0
    
    for obra in obras:
        for campo in campos_fuente:
            if campo in obra and obra[campo] == VALOR_VIEJO:
                obra[campo] = VALOR_NUEVO
                contador_cambios += 1
                break
    
    # Guardar JSON
    print(f"💾 Guardando cambios en {json_path}...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON actualizado: {contador_cambios} cambios realizados")
    return contador_cambios


def actualizar_supabase(dry_run: bool = False):
    """Actualiza Supabase"""
    print(f"\n{'='*60}")
    print("🗄️  ACTUALIZANDO SUPABASE")
    print(f"{'='*60}")
    
    try:
        client = get_supabase_client()
        
        # Primero contar cuántas obras tienen FUENTESXI
        print(f"🔍 Contando obras con '{VALOR_VIEJO}' en Supabase...")
        
        # Obtener todas las obras con FUENTESXI (con paginación)
        obras_afectadas = []
        offset = 0
        page_size = 1000
        
        while True:
            response = client.table('obras').select('id, titulo, fuente').eq('fuente', VALOR_VIEJO).range(offset, offset + page_size - 1).execute()
            
            if not response.data:
                break
            
            obras_afectadas.extend(response.data)
            
            if len(response.data) < page_size:
                break
            
            offset += page_size
        
        total_afectadas = len(obras_afectadas)
        print(f"📊 Encontradas {total_afectadas} obras con '{VALOR_VIEJO}'")
        
        if total_afectadas == 0:
            print("✅ No hay obras para actualizar en Supabase")
            return 0
        
        # Mostrar algunas obras afectadas
        print(f"\n📋 Primeras obras afectadas:")
        for obra in obras_afectadas[:10]:
            titulo = obra.get('titulo', 'Sin título')[:50]
            print(f"  - ID: {obra.get('id')}, Título: {titulo}...")
        if total_afectadas > 10:
            print(f"  ... y {total_afectadas - 10} más")
        
        if dry_run:
            print("\n🔍 DRY RUN: No se realizarán cambios")
            return total_afectadas
        
        # Confirmar (solo si no hay flag --yes)
        import sys
        if '--yes' not in sys.argv and '-y' not in sys.argv:
            print(f"\n⚠️  Se actualizarán {total_afectadas} obras en Supabase")
            respuesta = input("¿Continuar? (s/n): ").strip().lower()
            if respuesta != 's':
                print("❌ Operación cancelada")
                return 0
        else:
            print(f"\n⚠️  Actualizando {total_afectadas} obras en Supabase (--yes activado)")
        
        # Actualizar en lotes
        print(f"\n🔄 Actualizando obras en Supabase...")
        batch_size = 100
        total_actualizadas = 0
        
        for i in range(0, total_afectadas, batch_size):
            batch = obras_afectadas[i:i + batch_size]
            ids = [obra['id'] for obra in batch]
            
            # Actualizar usando UPDATE con filtro
            response = client.table('obras').update({'fuente': VALOR_NUEVO}).in_('id', ids).execute()
            
            if response.data:
                total_actualizadas += len(batch)
                print(f"  ✅ Lote {i // batch_size + 1}: {len(batch)} obras actualizadas")
            else:
                print(f"  ⚠️  Lote {i // batch_size + 1}: No se pudo actualizar")
        
        print(f"\n✅ Supabase actualizado: {total_actualizadas} obras modificadas")
        return total_actualizadas
        
    except Exception as e:
        print(f"❌ Error actualizando Supabase: {e}")
        import traceback
        traceback.print_exc()
        return 0


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Corregir FUENTESXI a Fuentes IX')
    parser.add_argument('--json', default='datos_obras.json', help='Ruta al archivo JSON')
    parser.add_argument('--dry-run', action='store_true', help='Solo mostrar cambios sin aplicarlos')
    parser.add_argument('--solo-json', action='store_true', help='Solo actualizar JSON, no Supabase')
    parser.add_argument('--solo-supabase', action='store_true', help='Solo actualizar Supabase, no JSON')
    
    args = parser.parse_args()
    
    json_path = Path(args.json)
    
    if not json_path.exists():
        print(f"❌ Error: No se encontró {json_path}")
        sys.exit(1)
    
    print("="*60)
    print("🔧 CORRECCIÓN DE FUENTE: FUENTESXI → Fuentes IX")
    print("="*60)
    print(f"Valor antiguo: '{VALOR_VIEJO}'")
    print(f"Valor nuevo: '{VALOR_NUEVO}'")
    print(f"Modo: {'DRY RUN' if args.dry_run else 'ACTUALIZACIÓN'}")
    print("="*60)
    
    cambios_json = 0
    cambios_supabase = 0
    
    # Actualizar JSON
    if not args.solo_supabase:
        cambios_json = actualizar_json(json_path, dry_run=args.dry_run)
    else:
        print("\n⏭️  Saltando actualización de JSON (--solo-supabase)")
    
    # Actualizar Supabase
    if not args.solo_json:
        cambios_supabase = actualizar_supabase(dry_run=args.dry_run)
    else:
        print("\n⏭️  Saltando actualización de Supabase (--solo-json)")
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)
    print(f"JSON: {cambios_json} cambios")
    print(f"Supabase: {cambios_supabase} cambios")
    print("="*60)
    
    if args.dry_run:
        print("\n💡 Ejecuta sin --dry-run para aplicar los cambios")
    else:
        print("\n✅ Proceso completado")


if __name__ == '__main__':
    main()

