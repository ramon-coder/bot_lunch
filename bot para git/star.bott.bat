@echo off
title Instalador Sistema de Almuerzo
color 0b

echo ==================================================
echo      INSTALANDO SISTEMA DE ALMUERZO
echo ==================================================
echo.

:: 1. INSTALAR DEPENDENCIAS
echo [+] Paso 1: Instalando Playwright...
python -m pip install playwright --quiet

:: 2. CONFIGURAR EL BOT EN EL INICIO
echo [+] Paso 2: Configurando el Bot para inicio automatico...
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
:: Corregido para usar el nombre del script de fondo
copy /y "bot_almuerzo.exe" "%STARTUP_FOLDER%\"

:: 3. COLOCAR EL CONFIGURADOR EN EL ESCRITORIO
echo [+] Paso 3: Colocando el Configurador en el Escritorio...
copy /y "configurador.exe" "%USERPROFILE%\Desktop\"

:: 4. EJECUTAR EL BOT POR PRIMERA VEZ
echo [+] Paso 4: Iniciando el bot en segundo plano...
start "" "%STARTUP_FOLDER%\bot_almuerzo.exe"

echo.
echo ==================================================
echo      INSTALACION COMPLETADA CON EXITO
echo ==================================================
pause