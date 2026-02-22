# 🍱 Sistema de Almuerzo Automático

¡Olvídate de llenar el formulario de almuerzo todos los días! Este proyecto automatiza el proceso utilizando **Python** y **Playwright**, permitiéndote configurar tus preferencias una sola vez y dejar que el bot trabaje por ti en segundo plano.
<img width="411" height="738" alt="Sin título" src="https://github.com/user-attachments/assets/a8e00af7-311a-4ccb-9fc6-3d7ca1916fa9" />


## ✨ Características
* **Automatización Invisible:** El bot se ejecuta en segundo plano sin interrumpir tu trabajo.
* **Interfaz Amigable:** Incluye un configurador visual (Tkinter) para cambiar sede, comentarios y estrellas.
* **Sesión Persistente:** Solo inicias sesión una vez; el bot guarda tu sesión de Microsoft de forma segura en tu PC local.
* **Inicio Automático:** Se configura para arrancar junto con Windows.
* **Confirmación por Correo:** Opción para activar/desactivar el correo de confirmación de Microsoft Forms.

## 🚀 Instalación (Para Usuarios)
Si solo quieres usar el programa, sigue estos pasos:

1. **Descarga los archivos:** Asegúrate de tener `bot-lunch.exe`, `interfaz-bot.exe` y `star.bott.bat` en la misma carpeta.
2. **Ejecuta el Instalador:** Haz doble clic en `star.bott.bat`. Se instalarán las dependencias necesarias y se creará un acceso directo en tu escritorio.
3. **Configura tu cuenta:**
   - Abre el **Configurador** desde tu escritorio.
   - Haz clic en **"1. CONECTAR CUENTA MICROSOFT"**.
   - Inicia sesión en la ventana de Chrome que aparece y ciérrala cuando veas el formulario de almuerzo.
   - Elige tu sede, estrellas y comentarios, luego dale a **"GUARDAR CAMBIOS"**.

## 🛠️ Requisitos para Desarrolladores
Si quieres modificar el código, necesitarás:
* Python 3.10+
* Playwright (`pip install playwright`)
* Tkinter (incluido en Python)

Comando para instalar el navegador del bot:
```bash
python -m playwright install chromium

⚠️ Seguridad y Privacidad
IMPORTANTE: Este bot guarda un "token" de sesión en la carpeta local %APPDATA%/bot_almuerzo_session.

Nunca compartas esa carpeta con nadie.

El archivo .gitignore de este repositorio ya está configurado para que no subas accidentalmente tus datos privados a GitHub.

🗑️ Desinstalación
Cierra el proceso bot-lunch.exe desde el Administrador de Tareas.

Borra el archivo de la carpeta de Inicio de Windows (%appdata%\Microsoft\Windows\Start Menu\Programs\Startup).

Borra la carpeta de datos en %appdata%\bot_almuerzo_session.

Desarrollado con ❤️ para ahorrar tiempo en la oficina.
