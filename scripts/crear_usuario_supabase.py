#!/usr/bin/env python3
"""
Script para crear un usuario manualmente en Supabase
Uso: python scripts/crear_usuario_supabase.py
"""

import os
import sys
import requests
import json

# Configuración de Supabase
# ⚠️ REEMPLAZA ESTOS VALORES CON TUS CREDENCIALES DE SUPABASE
SUPABASE_URL = 'https://kyxxpoewwjixbpcezays.supabase.co'
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ Error: No se encontró SUPABASE_SERVICE_ROLE_KEY")
    print("\n📋 Para obtener la Service Role Key:")
    print("1. Ve a Supabase Dashboard → Settings → API")
    print("2. Copia la 'service_role' key (NO la 'anon' key)")
    print("3. Ejecuta: export SUPABASE_SERVICE_ROLE_KEY='tu-service-role-key'")
    print("4. O edita este archivo y pégala directamente en la línea siguiente (solo para desarrollo)")
    print("\n💡 Alternativa: Usa el método manual desde Supabase Dashboard")
    print("   Ve a Authentication → Users → Add user")
    print("   Ver: CREAR_USUARIO_PACO_RAPIDO.md")
    
    # Opción para pegar la key directamente aquí (solo desarrollo)
    # SUPABASE_SERVICE_ROLE_KEY = 'pega-tu-service-role-key-aqui'
    
    sys.exit(1)

def crear_usuario_supabase(email, password, nombre_completo=None, confirmar_email=True):
    """
    Crea un usuario en Supabase usando la API Admin
    """
    url = f"{SUPABASE_URL}/auth/v1/admin/users"
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Datos del usuario
    user_data = {
        'email': email,
        'password': password,
        'email_confirm': confirmar_email,  # Si es True, el email queda confirmado automáticamente
        'user_metadata': {
            'nombre_completo': nombre_completo or email.split('@')[0]
        }
    }
    
    print(f"🔄 Creando usuario: {email}...")
    
    try:
        response = requests.post(url, headers=headers, json=user_data)
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Usuario creado exitosamente!")
            print(f"   ID: {user.get('id')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Confirmado: {user.get('email_confirmed_at') is not None}")
            
            # El trigger de Supabase debería crear el perfil automáticamente
            print(f"\n📝 El perfil se creará automáticamente gracias al trigger de Supabase")
            print(f"   Nombre completo: {nombre_completo or email.split('@')[0]}")
            print(f"   Rol: colaborador")
            
            return user
        else:
            print(f"❌ Error al crear usuario: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def verificar_perfil(usuario_id):
    """
    Verifica si el perfil fue creado correctamente
    """
    url = f"{SUPABASE_URL}/rest/v1/perfiles_usuarios?id=eq.{usuario_id}&select=*"
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            perfiles = response.json()
            if perfiles:
                print(f"\n✅ Perfil verificado:")
                print(f"   {json.dumps(perfiles[0], indent=2, ensure_ascii=False)}")
                return True
            else:
                print(f"\n⚠️  El perfil no se creó automáticamente")
                print(f"   Puedes crearlo manualmente ejecutando:")
                print(f"   INSERT INTO public.perfiles_usuarios (id, nombre_completo, rol)")
                print(f"   VALUES ('{usuario_id}', 'paco', 'colaborador');")
                return False
    except Exception as e:
        print(f"⚠️  No se pudo verificar el perfil: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🔐 Crear Usuario en Supabase")
    print("=" * 60)
    print()
    
    # Crear usuario "paco"
    email = 'paco@example.com'  # Cambia esto si quieres otro email
    password = '12345678'
    nombre_completo = 'paco'
    
    print(f"📋 Datos del usuario a crear:")
    print(f"   Email: {email}")
    print(f"   Contraseña: {password}")
    print(f"   Nombre completo: {nombre_completo}")
    print()
    
    # Crear usuario
    usuario = crear_usuario_supabase(
        email=email,
        password=password,
        nombre_completo=nombre_completo,
        confirmar_email=True  # El email queda confirmado automáticamente
    )
    
    if usuario:
        usuario_id = usuario.get('id')
        
        # Esperar un momento para que el trigger se ejecute
        import time
        print("\n⏳ Esperando a que se cree el perfil...")
        time.sleep(2)
        
        # Verificar perfil
        verificar_perfil(usuario_id)
        
        print("\n" + "=" * 60)
        print("✅ ¡Usuario creado exitosamente!")
        print("=" * 60)
        print(f"\n📧 Puedes iniciar sesión con:")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
    else:
        print("\n❌ No se pudo crear el usuario")
        sys.exit(1)
