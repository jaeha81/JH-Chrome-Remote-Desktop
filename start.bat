@echo off
cd /d %~dp0

:: 1. cloudflared 터널 시작 (로그 파일로 출력)
start "cloudflared" /min cmd /c "D:\cloudflared\cloudflared.exe tunnel --url http://localhost:8080 > %~dp0cloudflared.log 2>&1"

:: 2. URL 추출될 때까지 대기 (최대 15초)
set TUNNEL_URL=
set COUNT=0
:WAIT_URL
timeout /t 1 /nobreak >nul
set /a COUNT+=1
for /f "tokens=*" %%i in ('findstr "trycloudflare.com" "%~dp0cloudflared.log" 2^>nul') do (
    for /f "tokens=8" %%j in ("%%i") do set TUNNEL_URL=%%j
)
if "%TUNNEL_URL%"=="" (
    if %COUNT% lss 15 goto WAIT_URL
)

:: 3. .env 파일의 WEBHOOK_URL 업데이트
if not "%TUNNEL_URL%"=="" (
    powershell -Command "(Get-Content '%~dp0.env') -replace 'WEBHOOK_URL=.*', 'WEBHOOK_URL=%TUNNEL_URL%' | Set-Content '%~dp0.env'"
    echo [Tunnel] URL 업데이트: %TUNNEL_URL%
) else (
    echo [Tunnel] URL 추출 실패 - 기존 .env 유지
)

:: 4. 봇 서버 시작
call %~dp0.venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8080
