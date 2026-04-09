#!/usr/bin/env python3
"""
Script para corregir el valor "FUENTESXI" a "Fuentes IX" en el JSON local.
"""

import json
import sys
from pathlib import Path

# Valores a cambiar
VALOR_VIEJO = "FUENTESXI"
VALOR_NUEVO = "Fuentes IX"

def actualizar_json(json_path: Path, dry_run: bool = False):
    """Actualiza el JSON local"""
    print(f"\n{'='*60}")
    print("ACTUALIZANDO JSON LOCAL")
    print(f"{'='*60}")

    print(f"Cargando {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    obras = data.get('obras', []) if isinstance(data, dict) else data
    if not isinstance(obras, list):
        print("Error: El JSON no tiene el formato esperado")
        return 0

    contador_antes = 0
    obras_afectadas = []

    for i, obra in enumerate(obras):
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
                break

    print(f"Encontradas {contador_antes} ocurrencias de '{VALOR_VIEJO}'")

    if contador_antes == 0:
        print("No hay ocurrencias para corregir")
        return 0

    print(f"\nPrimeras obras afectadas:")
    for obra_info in obras_afectadas[:10]:
        print(f"  - ID: {obra_info['id']}, Título: {obra_info['titulo'][:50]}...")
    if len(obras_afectadas) > 10:
        print(f"  ... y {len(obras_afectadas) - 10} más")

    if dry_run:
        print("\nDRY RUN: No se realizarán cambios")
        return contador_antes

    print(f"\nReemplazando '{VALOR_VIEJO}' por '{VALOR_NUEVO}'...")
    contador_cambios = 0
    campos_fuente = ['fuente', 'Fuente Principal', 'Fuente', 'FUENTE']

    for obra in obras:
        for campo in campos_fuente:
            if campo in obra and obra[campo] == VALOR_VIEJO:
                obra[campo] = VALOR_NUEVO
                contador_cambios += 1
                break

    print(f"Guardando cambios en {json_path}...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"JSON actualizado: {contador_cambios} cambios realizados")
    return contador_cambios


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Corregir FUENTESXI a Fuentes IX')
    parser.add_argument('--json', default='datos_obras.json', help='Ruta al archivo JSON')
    parser.add_argument('--dry-run', action='store_true', help='Solo mostrar cambios sin aplicarlos')

    args = parser.parse_args()
    json_path = Path(args.json)

    if not json_path.exists():
        print(f"Error: No se encontró {json_path}")
        sys.exit(1)

    print("="*60)
    print("CORRECCIÓN DE FUENTE: FUENTESXI -> Fuentes IX")
    print("="*60)
    print(f"Valor antiguo: '{VALOR_VIEJO}'")
    print(f"Valor nuevo: '{VALOR_NUEVO}'")
    print(f"Modo: {'DRY RUN' if args.dry_run else 'ACTUALIZACIÓN'}")
    print("="*60)

    cambios_json = actualizar_json(json_path, dry_run=args.dry_run)

    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print(f"JSON: {cambios_json} cambios")
    print("="*60)

    if args.dry_run:
        print("\nEjecuta sin --dry-run para aplicar los cambios")
    else:
        print("\nProceso completado")


if __name__ == '__main__':
    main()
