"""
Script de testing automatizado para verificar que los cambios de admin persisten
Después de recargar la página.

Uso:
    python scripts/test_edicion_persistencia.py --url http://localhost:8000 --email admin@example.com
"""

import argparse
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        USE_WEBDRIVER_MANAGER = True
    except ImportError:
        USE_WEBDRIVER_MANAGER = False
except ImportError:
    print("❌ Selenium no está instalado. Instala con: pip install selenium webdriver-manager")
    exit(1)


class TestEdicionPersistencia:
    """Clase para probar la persistencia de cambios de admin"""
    
    def __init__(self, url: str, email: str, password: Optional[str] = None, headless: bool = False):
        self.url = url
        self.email = email
        self.password = password
        self.headless = headless
        self.driver = None
        self.test_results = []
        
    def setup_driver(self):
        """Configura el driver de Selenium"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            if USE_WEBDRIVER_MANAGER:
                from selenium.webdriver.chrome.service import Service
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.implicitly_wait(10)
            # Ejecutar script para ocultar que es un bot
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            })
            print("✅ Driver de Chrome configurado correctamente")
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            if not USE_WEBDRIVER_MANAGER:
                print("   Instala webdriver-manager para manejo automático:")
                print("   pip install webdriver-manager")
                print("   O instala ChromeDriver manualmente:")
                print("   macOS: brew install chromedriver")
                print("   Linux: sudo apt-get install chromium-chromedriver")
            raise
    
    def log_test(self, test_name: str, success: bool, message: str = "", details: Dict = None):
        """Registra el resultado de un test"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
        if details:
            print(f"   Detalles: {json.dumps(details, indent=2)}")
    
    def test_cargar_pagina(self) -> bool:
        """Test 1: Cargar la página inicial"""
        try:
            print("\n🔍 Test 1: Cargar página inicial...")
            self.driver.get(self.url)
            time.sleep(2)
            
            # Verificar que la página cargó
            if "DELIA" in self.driver.title or "Comedia" in self.driver.page_source:
                self.log_test("Cargar página", True, "Página cargada correctamente")
                return True
            else:
                self.log_test("Cargar página", False, "Página no contiene contenido esperado")
                return False
        except Exception as e:
            self.log_test("Cargar página", False, f"Error: {str(e)}")
            return False
    
    def test_login(self) -> bool:
        """Test 2: Hacer login como admin"""
        try:
            print("\n🔍 Test 2: Hacer login...")
            print(f"   Email: {self.email}")
            print(f"   Usando contraseña: {'Sí' if self.password else 'No (magic link)'}")
            
            # Esperar a que la página cargue completamente
            time.sleep(2)
            
            # Buscar campo de email - puede estar oculto inicialmente
            try:
                email_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "login-email"))
                )
            except TimeoutException:
                # Intentar buscar por otros selectores
                try:
                    email_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                except:
                    email_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='email' i]")
            
            # Asegurar que el campo esté visible y habilitado
            self.driver.execute_script("arguments[0].scrollIntoView(true);", email_input)
            time.sleep(0.5)
            
            # Limpiar y escribir email
            email_input.clear()
            time.sleep(0.3)
            email_input.send_keys(self.email)
            time.sleep(0.5)
            
            print(f"   ✅ Email ingresado: {self.email}")
            
            # Si hay contraseña, usarla; si no, usar magic link
            if self.password:
                print("   🔐 Usando login con contraseña...")
                try:
                    password_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, "login-password"))
                    )
                    password_input.clear()
                    time.sleep(0.3)
                    password_input.send_keys(self.password)
                    time.sleep(0.5)
                    print("   ✅ Contraseña ingresada")
                    
                    # Buscar y hacer clic en el botón de login
                    # El botón tiene onclick="handleLogin()" y texto "Entrar"
                    try:
                        # Intentar por texto del botón
                        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
                    except:
                        try:
                            # Intentar por onclick
                            login_button = self.driver.find_element(By.XPATH, "//button[contains(@onclick, 'handleLogin')]")
                        except:
                            # Intentar cualquier botón después del campo de contraseña
                            login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='password'] + button, input[type='password'] ~ button")
                    
                    # Asegurar que el botón esté visible
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
                    time.sleep(0.5)
                    
                    login_button.click()
                    print("   ✅ Botón de login presionado")
                    
                except Exception as e:
                    self.log_test("Login", False, f"Error con contraseña: {str(e)}")
                    return False
            else:
                # Usar magic link
                print("   📧 Usando magic link...")
                try:
                    magic_link_button = self.driver.find_element(By.ID, "magic-link-button")
                    magic_link_button.click()
                    print("   ⚠️  Magic link enviado. Esperando confirmación...")
                    print("   ⚠️  Por favor, confirma el login manualmente y presiona Enter")
                    input("   Presiona Enter después de confirmar el login...")
                except Exception as e:
                    self.log_test("Login", False, f"Error con magic link: {str(e)}")
                    return False
            
            # Esperar a que aparezca el botón de logout o algún elemento que indique login exitoso
            print("   ⏳ Esperando confirmación de login...")
            time.sleep(5)  # Dar más tiempo para el login
            
            # Verificar que el login fue exitoso
            try:
                logout_button = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.ID, "logout-button"))
                )
                self.log_test("Login", True, f"Login exitoso como {self.email}")
                return True
            except TimeoutException:
                # Intentar verificar de otra forma
                page_source_lower = self.driver.page_source.lower()
                if "logout" in page_source_lower or "cerrar sesión" in page_source_lower or "cerrar sesion" in page_source_lower:
                    self.log_test("Login", True, "Login exitoso (verificado por contenido)")
                    return True
                else:
                    # Tomar screenshot para debug
                    try:
                        self.driver.save_screenshot("login_failed.png")
                        print("   📸 Screenshot guardado en login_failed.png")
                    except:
                        pass
                    
                    self.log_test("Login", False, "No se encontró indicador de login exitoso. Revisa login_failed.png")
                    print(f"   📄 Contenido de la página (primeros 500 chars): {self.driver.page_source[:500]}")
                    return False
                    
        except Exception as e:
            self.log_test("Login", False, f"Error durante login: {str(e)}")
            import traceback
            print(f"   Stack trace: {traceback.format_exc()}")
            return False
    
    def test_verificar_rol_admin(self) -> bool:
        """Test 3: Verificar que el usuario es admin"""
        try:
            print("\n🔍 Test 3: Verificar rol admin...")
            
            # Buscar botón de admin o indicador de rol
            time.sleep(2)
            page_source = self.driver.page_source.lower()
            
            # Verificar en consola del navegador
            console_logs = self.driver.get_log('browser')
            es_admin = False
            
            for log in console_logs:
                if 'admin' in log['message'].lower() and 'true' in log['message'].lower():
                    es_admin = True
                    break
            
            # También verificar en el DOM
            if not es_admin:
                try:
                    admin_button = self.driver.find_element(By.ID, "admin-button")
                    es_admin = True
                except NoSuchElementException:
                    pass
            
            if es_admin or "admin" in page_source:
                self.log_test("Verificar rol admin", True, "Usuario es admin")
                return True
            else:
                self.log_test("Verificar rol admin", False, "No se pudo verificar que el usuario es admin")
                return False
                
        except Exception as e:
            self.log_test("Verificar rol admin", False, f"Error: {str(e)}")
            return False
    
    def test_activar_modo_edicion(self) -> bool:
        """Test 4: Activar modo edición"""
        try:
            print("\n🔍 Test 4: Activar modo edición...")
            
            # Buscar y hacer clic en el botón de modo edición
            modo_edicion_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "modo-edicion-toggle"))
            )
            modo_edicion_button.click()
            time.sleep(1)
            
            self.log_test("Activar modo edición", True, "Modo edición activado")
            return True
            
        except Exception as e:
            self.log_test("Activar modo edición", False, f"Error: {str(e)}")
            return False
    
    def test_editar_campo(self) -> Dict[str, Any]:
        """Test 5: Editar un campo de una obra"""
        try:
            print("\n🔍 Test 5: Editar campo...")
            
            # Buscar la primera fila de la tabla
            time.sleep(2)
            primera_fila = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr:first-child"))
            )
            
            # Obtener el ID de la obra desde la primera celda
            primera_celda = primera_fila.find_element(By.CSS_SELECTOR, "td:first-child")
            obra_id = primera_celda.text.strip()
            
            # Hacer clic en la fila para abrir el modal
            primera_fila.click()
            time.sleep(2)
            
            # Buscar el modal de detalle
            modal = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "modal-detalle"))
            )
            
            # Buscar el primer botón de editar (campo "titulo")
            try:
                boton_editar = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-campo='titulo']"))
                )
                
                # Obtener valor anterior
                valor_anterior = boton_editar.get_attribute("data-valor") or ""
                
                # Hacer clic en editar
                boton_editar.click()
                time.sleep(1)
                
                # Esperar el prompt y manejarlo
                # Nota: Selenium no puede manejar prompt() directamente, así que usamos JavaScript
                nuevo_valor = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Sobrescribir window.prompt ANTES de hacer clic
                self.driver.execute_script(f"""
                    window.prompt = function() {{
                        return '{nuevo_valor}';
                    }};
                """)
                
                # Hacer clic para activar el prompt (que ahora retornará nuestro valor)
                boton_editar.click()
                time.sleep(3)  # Esperar más tiempo para que se procese
                
                # Verificar que se cerró el prompt (esperando que aparezca un alert o cambio en el DOM)
                try:
                    WebDriverWait(self.driver, 5).until(
                        lambda d: nuevo_valor in d.page_source or d.switch_to.alert
                    )
                    # Si hay un alert, aceptarlo
                    try:
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except:
                        pass
                except:
                    pass
                
                # Verificar que el cambio se aplicó
                # Buscar el nuevo valor en el modal
                modal_source = modal.get_attribute('innerHTML')
                
                resultado = {
                    'obra_id': obra_id,
                    'campo': 'titulo',
                    'valor_anterior': valor_anterior,
                    'valor_nuevo': nuevo_valor,
                    'cambio_aplicado': nuevo_valor in modal_source or nuevo_valor in self.driver.page_source
                }
                
                if resultado['cambio_aplicado']:
                    self.log_test("Editar campo", True, f"Campo editado: {nuevo_valor}", resultado)
                else:
                    self.log_test("Editar campo", False, "Cambio no se reflejó en la UI", resultado)
                
                return resultado
                
            except TimeoutException:
                self.log_test("Editar campo", False, "No se encontró botón de editar")
                return {'error': 'No se encontró botón de editar'}
                
        except Exception as e:
            self.log_test("Editar campo", False, f"Error: {str(e)}")
            return {'error': str(e)}
    
    def test_recargar_pagina(self) -> bool:
        """Test 6: Recargar la página"""
        try:
            print("\n🔍 Test 6: Recargar página...")
            
            # Guardar el estado actual
            estado_antes = self.driver.page_source
            
            # Recargar
            self.driver.refresh()
            time.sleep(5)  # Esperar a que cargue
            
            # Verificar que se recargó
            estado_despues = self.driver.page_source
            
            if estado_antes != estado_despues:
                self.log_test("Recargar página", True, "Página recargada correctamente")
                return True
            else:
                self.log_test("Recargar página", False, "Página no se recargó")
                return False
                
        except Exception as e:
            self.log_test("Recargar página", False, f"Error: {str(e)}")
            return False
    
    def test_verificar_cambio_persiste(self, cambio_info: Dict[str, Any]) -> bool:
        """Test 7: Verificar que el cambio persiste después de recargar"""
        try:
            print("\n🔍 Test 7: Verificar persistencia del cambio...")
            
            if 'error' in cambio_info:
                self.log_test("Verificar persistencia", False, "No se puede verificar porque no hubo cambio previo")
                return False
            
            obra_id = cambio_info.get('obra_id')
            valor_nuevo = cambio_info.get('valor_nuevo')
            
            # Buscar la obra en la tabla después de recargar
            time.sleep(2)
            
            # Buscar la fila con el ID de la obra
            try:
                fila_obra = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[text()='{obra_id}']/.."))
                )
                
                # Hacer clic para abrir el modal
                fila_obra.click()
                time.sleep(2)
                
                # Buscar el valor en el modal
                modal = self.driver.find_element(By.ID, "modal-detalle")
                modal_source = modal.get_attribute('innerHTML')
                
                # Verificar que el valor nuevo está presente
                if valor_nuevo in modal_source or valor_nuevo in self.driver.page_source:
                    self.log_test("Verificar persistencia", True, 
                                f"Cambio persiste: {valor_nuevo} encontrado después de recargar",
                                {'obra_id': obra_id, 'valor_buscado': valor_nuevo})
                    return True
                else:
                    self.log_test("Verificar persistencia", False,
                                f"Cambio NO persiste: {valor_nuevo} NO encontrado después de recargar",
                                {'obra_id': obra_id, 'valor_buscado': valor_nuevo})
                    return False
                    
            except TimeoutException:
                self.log_test("Verificar persistencia", False, f"No se encontró la obra con ID {obra_id}")
                return False
                
        except Exception as e:
            self.log_test("Verificar persistencia", False, f"Error: {str(e)}")
            return False
    
    def ejecutar_todos_los_tests(self):
        """Ejecuta todos los tests en secuencia"""
        print("=" * 60)
        print("🧪 INICIANDO TESTS DE PERSISTENCIA DE CAMBIOS")
        print("=" * 60)
        
        try:
            self.setup_driver()
            
            # Ejecutar tests en orden
            if not self.test_cargar_pagina():
                return False
            
            if not self.test_login():
                return False
            
            if not self.test_verificar_rol_admin():
                print("⚠️  Advertencia: No se pudo verificar rol admin, continuando...")
            
            if not self.test_activar_modo_edicion():
                return False
            
            cambio_info = self.test_editar_campo()
            if 'error' in cambio_info:
                return False
            
            if not self.test_recargar_pagina():
                return False
            
            # Re-login después de recargar (si es necesario)
            time.sleep(2)
            if "login" in self.driver.page_source.lower() and "email" in self.driver.page_source.lower():
                print("\n⚠️  Se requiere login después de recargar...")
                if not self.test_login():
                    return False
            
            persistencia_ok = self.test_verificar_cambio_persiste(cambio_info)
            
            return persistencia_ok
            
        except Exception as e:
            print(f"\n❌ Error crítico durante los tests: {str(e)}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def generar_reporte(self, output_file: str = "test_report.json"):
        """Genera un reporte JSON con los resultados"""
        reporte = {
            'fecha': datetime.now().isoformat(),
            'url': self.url,
            'email': self.email,
            'total_tests': len(self.test_results),
            'tests_exitosos': sum(1 for t in self.test_results if t['success']),
            'tests_fallidos': sum(1 for t in self.test_results if not t['success']),
            'resultados': self.test_results
        }
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Reporte guardado en: {output_path}")
        return reporte


def main():
    parser = argparse.ArgumentParser(description='Test de persistencia de cambios de admin')
    parser.add_argument('--url', required=True, help='URL de la aplicación (ej: http://localhost:8000)')
    parser.add_argument('--email', required=True, help='Email del usuario admin')
    parser.add_argument('--password', help='Contraseña (opcional, si no se usa magic link)')
    parser.add_argument('--headless', action='store_true', help='Ejecutar en modo headless')
    parser.add_argument('--output', default='test_report.json', help='Archivo de salida para el reporte')
    
    args = parser.parse_args()
    
    tester = TestEdicionPersistencia(
        url=args.url,
        email=args.email,
        password=args.password,
        headless=args.headless
    )
    
    resultado = tester.ejecutar_todos_los_tests()
    reporte = tester.generar_reporte(args.output)
    
    print("\n" + "=" * 60)
    if resultado:
        print("✅ TODOS LOS TESTS PASARON")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
    print("=" * 60)
    
    print(f"\n📊 Resumen:")
    print(f"   Tests exitosos: {reporte['tests_exitosos']}/{reporte['total_tests']}")
    print(f"   Tests fallidos: {reporte['tests_fallidos']}/{reporte['total_tests']}")
    
    exit(0 if resultado else 1)


if __name__ == '__main__':
    main()

