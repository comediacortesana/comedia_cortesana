"""
Cliente para interactuar con Supabase
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
# Intentar cargar desde scripts/.env primero, luego desde raíz
env_paths = [
    Path(__file__).parent / '.env',
    Path(__file__).parent.parent / '.env',
    Path(__file__).parent / '.env.example'
]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break
else:
    # Si no encuentra ningún .env, intentar cargar desde variables de entorno del sistema
    load_dotenv()


def get_supabase_client() -> Client:
    """Crea y retorna un cliente de Supabase"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL y SUPABASE_KEY deben estar definidos en el archivo .env"
        )
    
    return create_client(supabase_url, supabase_key)


class SupabaseSync:
    """Clase para sincronizar datos con Supabase"""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    def get_all_obras(self) -> List[Dict[str, Any]]:
        """Obtiene todas las obras de Supabase (con paginación)"""
        all_obras = []
        page_size = 1000
        offset = 0
        
        while True:
            response = self.client.table('obras').select('*').range(offset, offset + page_size - 1).execute()
            if not response.data:
                break
            all_obras.extend(response.data)
            if len(response.data) < page_size:
                break
            offset += page_size
        
        return all_obras
    
    def get_obra_by_id(self, obra_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una obra por ID"""
        response = self.client.table('obras').select('*').eq('id', obra_id).execute()
        if response.data:
            return response.data[0]
        return None
    
    def create_obra(self, obra_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva obra"""
        response = self.client.table('obras').insert(obra_data).execute()
        if response.data:
            return response.data[0]
        raise Exception(f"Error al crear obra: {response}")
    
    def update_obra(self, obra_id: int, obra_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza una obra existente"""
        response = self.client.table('obras').update(obra_data).eq('id', obra_id).execute()
        if response.data:
            return response.data[0]
        raise Exception(f"Error al actualizar obra {obra_id}: {response}")
    
    def upsert_obra(self, obra_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea o actualiza una obra (upsert)"""
        response = self.client.table('obras').upsert(obra_data).execute()
        if response.data:
            return response.data[0]
        raise Exception(f"Error al hacer upsert de obra: {response}")
    
    def upsert_multiple_obras(
        self, 
        obras: List[Dict[str, Any]], 
        batch_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Hace upsert de múltiples obras en lotes"""
        results = []
        
        for i in range(0, len(obras), batch_size):
            batch = obras[i:i + batch_size]
            response = self.client.table('obras').upsert(batch).execute()
            if response.data:
                results.extend(response.data)
            else:
                print(f"Error en lote {i // batch_size + 1}")
        
        return results
    
    def get_pending_changes(self, estado: str = 'pendiente') -> List[Dict[str, Any]]:
        """Obtiene cambios pendientes"""
        response = self.client.table('cambios_pendientes').select('*').eq('estado', estado).execute()
        return response.data
    
    def approve_change(self, cambio_id: str, revisado_por: str) -> Dict[str, Any]:
        """Aprueba un cambio pendiente"""
        # Primero obtener el cambio
        cambio = self.client.table('cambios_pendientes').select('*').eq('id', cambio_id).execute()
        if not cambio.data:
            raise Exception(f"Cambio {cambio_id} no encontrado")
        
        cambio_data = cambio.data[0]
        
        # Aplicar el cambio a la obra
        obra_update = {cambio_data['campo']: cambio_data['valor_nuevo']}
        self.update_obra(cambio_data['obra_id'], obra_update)
        
        # Marcar el cambio como aprobado
        response = self.client.table('cambios_pendientes').update({
            'estado': 'aprobado',
            'revisado_por': revisado_por,
            'revisado_at': 'now()'
        }).eq('id', cambio_id).execute()
        
        return response.data[0] if response.data else None
    
    def reject_change(self, cambio_id: str, revisado_por: str, motivo: str = None) -> Dict[str, Any]:
        """Rechaza un cambio pendiente"""
        response = self.client.table('cambios_pendientes').update({
            'estado': 'rechazado',
            'revisado_por': revisado_por,
            'revisado_at': 'now()',
            'motivo_rechazo': motivo
        }).eq('id', cambio_id).execute()
        
        return response.data[0] if response.data else None


if __name__ == '__main__':
    # Ejemplo de uso
    sync = SupabaseSync()
    obras = sync.get_all_obras()
    print(f"Total de obras: {len(obras)}")

