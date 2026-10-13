@echo off
chcp 65001 >nul
:: Check for admin permissions
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

title Airtel Wi-Fi Fixer
echo ======================================================================
echo           Airtel Wi-Fi Latency & Band Fix (Permanent)
echo ======================================================================
echo.

echo [1/4] Disabling Wi-Fi Power Saving...
powershell -NoProfile -Command "Set-NetAdapterAdvancedProperty -Name 'Wi-Fi' -DisplayName 'Power Saving' -DisplayValue 'Disabled' -ErrorAction SilentlyContinue"
echo       [OK] Power Saving Disabled!

echo.
echo [2/4] Disabling Windows Fast Startup...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /v HiberbootEnabled /t REG_DWORD /d 0 /f >nul
echo       [OK] Fast Startup Disabled!

echo.
echo [3/4] Switching Preferred Band to 2.4GHz (Fixing 1700ms 5GHz lag)...
powershell -NoProfile -Command "Set-NetAdapterAdvancedProperty -Name 'Wi-Fi' -DisplayName 'Preferred Band' -DisplayValue '2. Prefer 2.4GHz band' -ErrorAction SilentlyContinue"
echo       [OK] Switched to 2.4GHz!

echo.
echo [4/4] Reconnecting to Airtel_die_8967...
netsh wlan disconnect >nul 2>&1
timeout /t 2 /nobreak >nul
netsh wlan connect name="Airtel_die_8967" >nul 2>&1
timeout /t 3 /nobreak >nul
echo       [OK] Wi-Fi Reconnected!

echo.
echo ======================================================================
echo Current Wi-Fi Status:
powershell -NoProfile -Command "netsh wlan show interfaces | Select-String -Pattern 'Band', 'Channel', 'Signal', 'State'"
echo ======================================================================
echo.
echo Sabhi settings successfully apply ho gayi hain!
echo.
pause
