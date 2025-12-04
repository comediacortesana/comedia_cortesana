"""
Script de diagnóstico para verificar por qué no cargan los datos desde Supabase
Hace scraping de la página y analiza los logs de la consola del navegador
"""

import argparse
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

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


class DiagnosticarCargaDatos:
    """Diagnóstico de carga de datos desde Supabase"""
    
    def __init__(self, url: str, headless: bool = False):
        self.url = url
        self.headless = headless
        self.driver = None
        self.diagnosticos = []
        
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
        
        # Habilitar logging de consola
        chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'performance': 'ALL'})
        
        try:
            if USE_WEBDRIVER_MANAGER:
                from selenium.webdriver.chrome.service import Service
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.implicitly_wait(10)
            print("✅ Driver de Chrome configurado correctamente")
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            raise
    
    def log_diagnostico(self, categoria: str, mensaje: str, detalles: Dict = None):
        """Registra un diagnóstico"""
        diagnostico = {
            'categoria': categoria,
            'mensaje': mensaje,
            'timestamp': datetime.now().isoformat(),
            'detalles': detalles or {}
        }
        self.diagnosticos.append(diagnostico)
        
        icono = {
            'ERROR': '❌',
            'WARNING': '⚠️',
            'INFO': 'ℹ️',
            'SUCCESS': '✅'
        }.get(categoria, '📋')
        
        print(f"{icono} [{categoria}] {mensaje}")
        if detalles:
            print(f"   Detalles: {json.dumps(detalles, indent=2, ensure_ascii=False)}")
    
    def diagnosticar_carga_pagina(self):
        """Diagnóstico 1: Cargar la página"""
        try:
            print("\n" + "="*60)
            print("🔍 DIAGNÓSTICO 1: Cargar página")
            print("="*60)
            
            self.driver.get(self.url)
            time.sleep(5)  # Esperar a que cargue
            
            if "DELIA" in self.driver.title or "Comedia" in self.driver.page_source:
                self.log_diagnostico('SUCCESS', 'Página cargada correctamente', {
                    'title': self.driver.title,
                    'url': self.driver.current_url
                })
                return True
            else:
                self.log_diagnostico('ERROR', 'Página no contiene contenido esperado', {
                    'title': self.driver.title,
                    'url': self.driver.current_url
                })
                return False
        except Exception as e:
            self.log_diagnostico('ERROR', f'Error cargando página: {str(e)}')
            return False
    
    def diagnosticar_consola_navegador(self):
        """Diagnóstico 2: Analizar logs de la consola del navegador"""
        try:
            print("\n" + "="*60)
            print("🔍 DIAGNÓSTICO 2: Analizar consola del navegador")
            print("="*60)
            
            # Obtener logs de la consola
            logs = self.driver.get_log('browser')
            
            errores = []
            warnings = []
            info_supabase = []
            info_carga = []
            
            for log in logs:
                message = log.get('message', '')
                level = log.get('level', '')
                
                if level == 'SEVERE' or 'error' in message.lower():
                    errores.append(message)
                elif level == 'WARNING' or 'warning' in message.lower() or '⚠️' in message:
                    warnings.append(message)
                elif 'supabase' in message.lower():
                    info_supabase.append(message)
                elif 'cargar' in message.lower() or 'carga' in message.lower() or 'loading' in message.lower():
                    info_carga.append(message)
            
            # Analizar errores
            if errores:
                self.log_diagnostico('ERROR', f'Se encontraron {len(errores)} errores en la consola', {
                    'errores': errores[:10]  # Primeros 10 errores
                })
            else:
                self.log_diagnostico('SUCCESS', 'No se encontraron errores en la consola')
            
            # Analizar warnings
            if warnings:
                self.log_diagnostico('WARNING', f'Se encontraron {len(warnings)} warnings', {
                    'warnings': warnings[:10]
                })
            
            # Analizar mensajes de Supabase
            if info_supabase:
                self.log_diagnostico('INFO', f'Mensajes relacionados con Supabase: {len(info_supabase)}', {
                    'mensajes': info_supabase[:10]
                })
            
            # Analizar mensajes de carga
            if info_carga:
                self.log_diagnostico('INFO', f'Mensajes relacionados con carga de datos: {len(info_carga)}', {
                    'mensajes': info_carga[:10]
                })
            
            return {
                'errores': errores,
                'warnings': warnings,
                'info_supabase': info_supabase,
                'info_carga': info_carga
            }
            
        except Exception as e:
            self.log_diagnostico('ERROR', f'Error analizando consola: {str(e)}')
            return {}
    
    def diagnosticar_estado_datos(self):
        """Diagnóstico 3: Verificar estado de los datos en la página"""
        try:
            print("\n" + "="*60)
            print("🔍 DIAGNÓSTICO 3: Verificar estado de datos en la página")
            print("="*60)
            
            time.sleep(3)  # Esperar a que se procese
            
            # Buscar mensajes sobre la fuente de datos
            page_source = self.driver.page_source.lower()
            
            fuente_datos = None
            if 'supabase' in page_source:
                fuente_datos = 'Supabase'
            elif 'github' in page_source:
                fuente_datos = 'GitHub'
            elif 'json' in page_source:
                fuente_datos = 'JSON local'
            
            # Buscar contador de resultados
            resultados_texto = None
            try:
                # Buscar texto como "X resultados encontrados" o "0 resultados"
                resultados_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'resultados') or contains(text(), 'resultados encontrados')]")
                resultados_texto = resultados_element.text
            except:
                pass
            
            # Buscar mensaje de carga
            mensaje_carga = None
            try:
                carga_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Cargando') or contains(text(), 'Loading')]")
                mensaje_carga = carga_element.text
            except:
                pass
            
            # Verificar si hay tabla de resultados
            hay_tabla = False
            num_filas = 0
            tabla_visible = False
            tabla_info = {}
            try:
                tabla = self.driver.find_element(By.TAG_NAME, "tbody")
                filas = tabla.find_elements(By.TAG_NAME, "tr")
                num_filas = len(filas)
                hay_tabla = True
                
                # Verificar si la tabla es visible
                tabla_visible = tabla.is_displayed()
                
                # Obtener información de estilo
                tabla_info = {
                    'visible': tabla_visible,
                    'display': tabla.value_of_css_property('display'),
                    'visibility': tabla.value_of_css_property('visibility'),
                    'opacity': tabla.value_of_css_property('opacity'),
                    'height': tabla.value_of_css_property('height'),
                    'width': tabla.value_of_css_property('width')
                }
            except Exception as e:
                tabla_info = {'error': str(e)}
            
            self.log_diagnostico('INFO', 'Estado de datos en la página', {
                'fuente_detectada': fuente_datos,
                'resultados_texto': resultados_texto,
                'mensaje_carga': mensaje_carga,
                'hay_tabla': hay_tabla,
                'num_filas_tabla': num_filas,
                'tabla_visible': tabla_visible,
                'tabla_info': tabla_info
            })
            
            return {
                'fuente_datos': fuente_datos,
                'resultados': resultados_texto,
                'mensaje_carga': mensaje_carga,
                'hay_tabla': hay_tabla,
                'num_filas': num_filas
            }
            
        except Exception as e:
            self.log_diagnostico('ERROR', f'Error verificando estado: {str(e)}')
            return {}
    
    def diagnosticar_supabase_conexion(self):
        """Diagnóstico 4: Verificar conexión a Supabase"""
        try:
            print("\n" + "="*60)
            print("🔍 DIAGNÓSTICO 4: Verificar conexión a Supabase")
            print("="*60)
            
            # Ejecutar JavaScript para verificar estado de Supabase
            estado_supabase = self.driver.execute_script("""
                // Verificar si supabase está disponible
                if (typeof window.supabase === 'undefined') {
                    return { disponible: false, error: 'Supabase no está disponible' };
                }
                
                // Intentar obtener sesión
                return window.supabase.auth.getSession()
                    .then(result => {
                        return {
                            disponible: true,
                            tiene_sesion: result.data.session !== null,
                            email_usuario: result.data.session?.user?.email || null,
                            error: result.error ? result.error.message : null
                        };
                    })
                    .catch(error => {
                        return {
                            disponible: true,
                            error: error.message
                        };
                    });
            """)
            
            # Esperar a que se resuelva la promesa
            time.sleep(2)
            
            # Intentar obtener el resultado de otra forma
            try:
                # Ejecutar código síncrono para verificar
                estado = self.driver.execute_script("""
                    return {
                        supabase_disponible: typeof window.supabase !== 'undefined',
                        supabase_url: typeof window.supabase !== 'undefined' ? window.supabase.supabaseUrl : null,
                        supabase_key: typeof window.supabase !== 'undefined' ? (window.supabase.supabaseKey ? 'presente' : 'ausente') : null
                    };
                """)
                
                self.log_diagnostico('INFO', 'Estado de Supabase en la página', estado)
                
            except Exception as e:
                self.log_diagnostico('WARNING', f'No se pudo verificar estado de Supabase: {str(e)}')
            
            return estado if 'estado' in locals() else {}
            
        except Exception as e:
            self.log_diagnostico('ERROR', f'Error verificando Supabase: {str(e)}')
            return {}
    
    def diagnosticar_carga_datos_funcion(self):
        """Diagnóstico 5: Verificar si cargarDatos() se ejecutó"""
        try:
            print("\n" + "="*60)
            print("🔍 DIAGNÓSTICO 5: Verificar ejecución de cargarDatos()")
            print("="*60)
            
            # Buscar en los logs de consola mensajes relacionados con cargarDatos
            logs = self.driver.get_log('browser')
            
            mensajes_cargar_datos = []
            mensajes_supabase = []
            mensajes_fallback = []
            
            for log in logs:
                message = log.get('message', '').lower()
                if 'cargar' in message and 'datos' in message:
                    mensajes_cargar_datos.append(log.get('message', ''))
                if 'supabase' in message and ('cargar' in message or 'load' in message):
                    mensajes_supabase.append(log.get('message', ''))
                if 'fallback' in message or 'json' in message or 'github' in message:
                    mensajes_fallback.append(log.get('message', ''))
            
            self.log_diagnostico('INFO', 'Mensajes relacionados con carga de datos', {
                'mensajes_cargar_datos': mensajes_cargar_datos[:5],
                'mensajes_supabase': mensajes_supabase[:5],
                'mensajes_fallback': mensajes_fallback[:5]
            })
            
            # Verificar si hay datos cargados en JavaScript
            try:
                datos_cargados = self.driver.execute_script("""
                    // Intentar acceder a las variables globales
                    if (typeof datosOriginales !== 'undefined') {
                        return {
                            datos_originales_length: datosOriginales.length,
                            datos_filtrados_length: typeof datosFiltrados !== 'undefined' ? datosFiltrados.length : 0,
                            metadata: typeof metadata !== 'undefined' ? metadata : null
                        };
                    }
                    return { error: 'Variables no disponibles' };
                """)
                
                self.log_diagnostico('INFO', 'Estado de variables de datos en JavaScript', datos_cargados)
                
            except Exception as e:
                self.log_diagnostico('WARNING', f'No se pudo acceder a variables JavaScript: {str(e)}')
            
            return {
                'mensajes_cargar_datos': mensajes_cargar_datos,
                'mensajes_supabase': mensajes_supabase,
                'mensajes_fallback': mensajes_fallback
            }
            
        except Exception as e:
            self.log_diagnostico('ERROR', f'Error verificando función: {str(e)}')
            return {}
    
    def ejecutar_diagnosticos(self):
        """Ejecuta todos los diagnósticos"""
        print("="*60)
        print("🔍 DIAGNÓSTICO DE CARGA DE DATOS")
        print("="*60)
        print(f"URL: {self.url}")
        print(f"Fecha: {datetime.now().isoformat()}")
        print("="*60)
        
        try:
            self.setup_driver()
            
            # Ejecutar diagnósticos en orden
            self.diagnosticar_carga_pagina()
            time.sleep(2)
            
            logs_consola = self.diagnosticar_consola_navegador()
            time.sleep(1)
            
            estado_datos = self.diagnosticar_estado_datos()
            time.sleep(1)
            
            estado_supabase = self.diagnosticar_supabase_conexion()
            time.sleep(1)
            
            estado_funcion = self.diagnosticar_carga_datos_funcion()
            
            # Resumen
            print("\n" + "="*60)
            print("📊 RESUMEN DE DIAGNÓSTICOS")
            print("="*60)
            
            errores_encontrados = sum(1 for d in self.diagnosticos if d['categoria'] == 'ERROR')
            warnings_encontrados = sum(1 for d in self.diagnosticos if d['categoria'] == 'WARNING')
            
            print(f"Total de diagnósticos: {len(self.diagnosticos)}")
            print(f"Errores encontrados: {errores_encontrados}")
            print(f"Warnings encontrados: {warnings_encontrados}")
            
            if estado_datos.get('num_filas', 0) > 0:
                print(f"✅ Datos cargados: {estado_datos['num_filas']} filas en la tabla")
            else:
                print("❌ No se encontraron datos cargados")
            
            if estado_datos.get('fuente_datos'):
                print(f"📊 Fuente detectada: {estado_datos['fuente_datos']}")
            
            return {
                'diagnosticos': self.diagnosticos,
                'resumen': {
                    'total': len(self.diagnosticos),
                    'errores': errores_encontrados,
                    'warnings': warnings_encontrados,
                    'datos_cargados': estado_datos.get('num_filas', 0),
                    'fuente_datos': estado_datos.get('fuente_datos')
                }
            }
            
        except Exception as e:
            self.log_diagnostico('ERROR', f'Error crítico durante diagnósticos: {str(e)}')
            return {'error': str(e)}
        finally:
            if self.driver:
                # Tomar screenshot antes de cerrar
                try:
                    self.driver.save_screenshot("diagnostico_screenshot.png")
                    print("\n📸 Screenshot guardado en: diagnostico_screenshot.png")
                except:
                    pass
                self.driver.quit()
    
    def generar_reporte(self, output_file: str = "diagnostico_carga_datos.json"):
        """Genera un reporte JSON con los resultados"""
        reporte = {
            'fecha': datetime.now().isoformat(),
            'url': self.url,
            'diagnosticos': self.diagnosticos,
            'resumen': {
                'total_diagnosticos': len(self.diagnosticos),
                'errores': sum(1 for d in self.diagnosticos if d['categoria'] == 'ERROR'),
                'warnings': sum(1 for d in self.diagnosticos if d['categoria'] == 'WARNING'),
                'success': sum(1 for d in self.diagnosticos if d['categoria'] == 'SUCCESS')
            }
        }
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Reporte guardado en: {output_path}")
        return reporte


def main():
    parser = argparse.ArgumentParser(description='Diagnóstico de carga de datos desde Supabase')
    parser.add_argument('--url', default='https://comediacortesana.github.io/comedia_cortesana/', 
                        help='URL de la aplicación')
    parser.add_argument('--headless', action='store_true', help='Ejecutar en modo headless')
    parser.add_argument('--output', default='diagnostico_carga_datos.json', 
                        help='Archivo de salida para el reporte')
    
    args = parser.parse_args()
    
    diagnostico = DiagnosticarCargaDatos(
        url=args.url,
        headless=args.headless
    )
    
    resultado = diagnostico.ejecutar_diagnosticos()
    reporte = diagnostico.generar_reporte(args.output)
    
    print("\n" + "="*60)
    if resultado.get('resumen', {}).get('errores', 0) > 0:
        print("⚠️ SE ENCONTRARON PROBLEMAS")
    else:
        print("✅ DIAGNÓSTICO COMPLETADO")
    print("="*60)
    
    exit(0 if resultado.get('resumen', {}).get('errores', 0) == 0 else 1)


if __name__ == '__main__':
    main()

