import os
import time
import json
import ctypes
import re
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

CONFIG_PATH = os.path.join(os.environ['APPDATA'], "bot_almuerzo_config.json")
SESSION_PATH = os.path.join(os.environ['APPDATA'], "bot_almuerzo_session")
URL_FORMULARIO = "https://forms.office.com/pages/responsepage.aspx?id=LNTN0lSCL0y4mNpKDygmQ77LOvhcurRDp3vowKIibipUMVNYWjhGOVBGWDZTNUM5QVg1MllDT1lIVS4u&route=shorturl"
HORA_INICIO_VENTANA = "15:40"
HORA_FIN_VENTANA = "10:00"

def mostrar_error_ventana(titulo, mensaje):
    ctypes.windll.user32.MessageBoxW(0, mensaje, titulo, 0x10)

def ejecutar_envio():
    if not os.path.exists(CONFIG_PATH): return False
    with open(CONFIG_PATH, "r") as f: config = json.load(f)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fotos_dir = os.path.join(base_dir, "comprobantes")
    if not os.path.exists(fotos_dir): os.makedirs(fotos_dir)

    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=SESSION_PATH, 
                headless=True, 
                channel="chrome"
            )
            page = browser.new_page()
            # Esperamos a que la página cargue
            page.goto(URL_FORMULARIO, wait_until="networkidle", timeout=60000)
            
            # --- COMPROBACIÓN MEJORADA (Evita el Timeout) ---
            # Usamos un selector flexible para el texto de la imagen
            texto_ya_enviado = re.compile(r"Su respuesta ya se ha enviado|solo admite una respuesta", re.I)
            
            try:
                # Esperamos solo 5 segundos para ver si el mensaje aparece
                # Si no aparece, saltará al bloque except y continuará con el llenado
                page.get_by_text(texto_ya_enviado).wait_for(state="visible", timeout=5000)
                
                print("Confirmado: El formulario ya fue enviado. Saltando...")
                nombre_foto = f"ya_estaba_enviado_{datetime.now().strftime('%Y-%m-%d')}.png"
                page.screenshot(path=os.path.join(fotos_dir, nombre_foto))
                return True # El día se marca como gestionado con éxito
                
            except:
                # Si el mensaje NO aparece en 5s, significa que el formulario está disponible
                print("Formulario listo para completar...")
                
            # Si no está enviado, procedemos con el llenado normal
            if "login.microsoftonline.com" in page.url:
                mostrar_error_ventana("Bot Almuerzo", "Sesión expirada. Abre el configurador.")
                return False

            # Llenado con selectores flexibles
            page.get_by_role("button", name=re.compile("Ubicación", re.I)).click()
            page.get_by_role("option", name=config["ubicacion"]).click()
            page.get_by_role("radio", name=config["estrellas"]).click()
            
            # Si aquí fallaba antes por Timeout, ahora ya no llegará si ya se envió
            page.get_by_role("textbox", name=re.compile("comentario", re.I)).fill(config["comentario"])

            # Evaluación de matriz
            try:
                page.get_by_role("radio", name=re.compile(f"Cocción {config['coccion']}", re.I)).click()
                page.get_by_role("radio", name=re.compile(f"Condimentos {config['condimentos']}", re.I)).click()
                page.get_by_role("radio", name=re.compile(f"Porción {config['porcion']}", re.I)).click()
            except: pass

            page.get_by_role("button", name=re.compile("asistir", re.I)).click()
            page.get_by_role("option", name=config["asistencia"]).click()
            
            page.get_by_role("button", name=re.compile("Enviar", re.I)).click()
            time.sleep(5)

            nombre_foto = f"exito_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.png"
            page.screenshot(path=os.path.join(fotos_dir, nombre_foto))
            return True

        except Exception as e:
            # Solo mostramos error si realmente es un fallo técnico y no la página de "Ya enviado"
            error_msg = str(e).splitlines()[0]
            mostrar_error_ventana("Error de Bot", f"No se pudo procesar el formulario:\n{error_msg}")
            return False
        finally:
            if browser: browser.close()

def bucle_principal():
    ultimo_dia_gestionado = None
    while True:
        ahora = datetime.now()
        hora_actual = ahora.strftime("%H:%M")
        
        if hora_actual >= HORA_INICIO_VENTANA:
            dia_objetivo = (ahora + timedelta(days=1)).strftime("%Y-%m-%d")
            en_ventana = True
        elif hora_actual <= HORA_FIN_VENTANA:
            dia_objetivo = ahora.strftime("%Y-%m-%d")
            en_ventana = True
        else:
            en_ventana = False

        if en_ventana and dia_objetivo != ultimo_dia_gestionado:
            if datetime.strptime(dia_objetivo, "%Y-%m-%d").weekday() < 5:
                if ejecutar_envio():
                    ultimo_dia_gestionado = dia_objetivo
                else:
                    time.sleep(300) 
            else:
                ultimo_dia_gestionado = dia_objetivo
        time.sleep(60)

if __name__ == "__main__":
    bucle_principal()