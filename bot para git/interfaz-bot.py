import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import re
from playwright.sync_api import sync_playwright

# Rutas universales - Usamos una carpeta específica para el BOT
CONFIG_PATH = os.path.join(os.environ['APPDATA'], "bot_almuerzo_config.json")
SESSION_PATH = os.path.join(os.environ['APPDATA'], "bot_almuerzo_session")

def limpiar_solo_bot():
    """Solo cierra procesos del bot, NO tu navegador Chrome personal."""
    try:
        os.system('taskkill /f /im configurador.exe /t >nul 2>&1')
        os.system('taskkill /f /im bot-lunch.exe /t >nul 2>&1')
    except:
        pass

def cargar_datos_iniciales():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except: pass
    return {
        "ubicacion": "Sede Excle", 
        "comentario": "bien", 
        "asistencia": "No", 
        "estrellas": "5 Star",
        "coccion": "Dentro de lo esperado",
        "condimentos": "Dentro de lo esperado",
        "porcion": "Dentro de lo esperado"
    }

def abrir_login():
    limpiar_solo_bot()
    messagebox.showinfo("Login Microsoft", "Se abrirá una ventana limpia de Chrome. Inicia sesión y ciérrala al terminar.")
    try:
        with sync_playwright() as p:
            # Usamos una sesión persistente aislada
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=SESSION_PATH,
                headless=False,
                channel="chrome" 
            )
            page = browser_context.new_page()
            page.goto("https://forms.office.com/pages/responsepage.aspx?id=LNTN0lSCL0y4mNpKDygmQ77LOvhcurRDp3vowKIibipUMVNYWjhGOVBGWDZTNUM5QVg1MllDT1lIVS4u&route=shorturl")
            
            while len(browser_context.pages) > 0:
                page.wait_for_timeout(1000)
            browser_context.close()
        messagebox.showinfo("Éxito", "Sesión guardada. Ya puedes cerrar esta ventana.")
    except Exception as e:
        messagebox.showerror("Error", f"Detalle: {str(e).splitlines()[0]}")

def guardar():
    data = {
        "ubicacion": combo_ub.get(),
        "comentario": ent_com.get(),
        "asistencia": combo_as.get(),
        "estrellas": str(scale_est.get()) + " Star",
        "coccion": combo_coc.get(),
        "condimentos": combo_con.get(),
        "porcion": combo_por.get()
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Guardado", "Configuración lista.")
    root.destroy()

if __name__ == "__main__":
    prev = cargar_datos_iniciales()
    root = tk.Tk()
    root.title("Configurador de Almuerzo")
    root.geometry("400x700")

    tk.Label(root, text="SISTEMA DE ALMUERZO", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(root, text="1. INICIAR SESIÓN MICROSOFT", command=abrir_login, bg="#0078d4", fg="white").pack(pady=5)

    tk.Label(root, text="2. OPCIONES", font=("Arial", 9, "bold")).pack(pady=10)

    tk.Label(root, text="Sede:").pack()
    sedes = ["Sede Excle", "CNE Plaza Venezuela", "SAIME Torre ACO Las Mercedes", "CNE Plaza Caracas", "UBV", "Mariche III", "PDVSA La Campiña", "Otras"]
    combo_ub = ttk.Combobox(root, values=sedes, state="readonly", width=35)
    combo_ub.set(prev.get("ubicacion", "Sede Excle"))
    combo_ub.pack()

    tk.Label(root, text="Estrellas:").pack(pady=5)
    scale_est = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, length=200)
    scale_est.set(int(prev.get("estrellas", "5 Star").split()[0]))
    scale_est.pack()

    opciones_m = ["Por encima de lo esperado", "Dentro de lo esperado", "Por debajo de lo esperado"]
    tk.Label(root, text="Cocción:").pack()
    combo_coc = ttk.Combobox(root, values=opciones_m, state="readonly")
    combo_coc.set(prev.get("coccion", "Dentro de lo esperado"))
    combo_coc.pack()

    tk.Label(root, text="Condimentos:").pack()
    combo_con = ttk.Combobox(root, values=opciones_m, state="readonly")
    combo_con.set(prev.get("condimentos", "Dentro de lo esperado"))
    combo_con.pack()

    tk.Label(root, text="Porción:").pack()
    combo_por = ttk.Combobox(root, values=opciones_m, state="readonly")
    combo_por.set(prev.get("porcion", "Dentro de lo esperado"))
    combo_por.pack()

    tk.Label(root, text="Comentario:").pack(pady=5)
    ent_com = tk.Entry(root, width=30)
    ent_com.insert(0, prev.get("comentario", "bien"))
    ent_com.pack()

    tk.Label(root, text="¿Asistirás?:").pack(pady=5)
    combo_as = ttk.Combobox(root, values=["Sí", "No"], state="readonly")
    combo_as.set(prev.get("asistencia", "No"))
    combo_as.pack()

    tk.Button(root, text="GUARDAR CAMBIOS", command=guardar, bg="#28a745", fg="white", font=("Arial", 10, "bold")).pack(pady=20)
    root.mainloop()