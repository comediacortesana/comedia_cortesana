-- ============================================================================
-- VERIFICAR Y CREAR TRIGGER PARA PERFILES AUTOMÁTICOS
-- ============================================================================
-- Ejecuta este SQL en Supabase SQL Editor
-- Esto crea el perfil automáticamente cuando alguien se registra

-- Función que se ejecuta cuando se crea un nuevo usuario
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.perfiles_usuarios (id, nombre_completo, rol)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'nombre_completo', NEW.email),
    'colaborador'
  )
  ON CONFLICT (id) DO NOTHING; -- Evitar errores si ya existe
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger que ejecuta la función cuando se crea un usuario en auth.users
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================================================
-- CREAR PERFIL MANUALMENTE PARA EL USUARIO EXISTENTE
-- ============================================================================
-- Si ya tienes un usuario registrado pero sin perfil, ejecuta esto:
-- (Reemplaza el UUID con el de tu usuario)

-- Primero, obtén el UUID de tu usuario desde Authentication > Users
-- Luego ejecuta:

-- INSERT INTO public.perfiles_usuarios (id, nombre_completo, rol)
-- VALUES (
--   'TU-UUID-AQUI',  -- ⚠️ Reemplaza con el UUID de tu usuario
--   'Tu Nombre',     -- ⚠️ Reemplaza con el nombre que quieras
--   'colaborador'
-- )
-- ON CONFLICT (id) DO NOTHING;

