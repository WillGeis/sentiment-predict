@echo off
set IMAGE_NAME=stock-trader
set CONTAINER_NAME=stock-trader-container

echo Checking if Docker Desktop is running...
tasklist | findstr /I "Docker Desktop" >nul
if errorlevel 1 (
    echo Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    echo Waiting for Docker to initialize...
    timeout /t 10 /nobreak >nul
    
    :CHECK_DOCKER
    docker info >nul 2>&1
    if errorlevel 1 (
        echo Docker is still starting, waiting...
        timeout /t 5 /nobreak >nul
        goto CHECK_DOCKER
    )
)

echo Building Docker image...
docker build -t %IMAGE_NAME% .

echo Checking for existing container...
docker ps -q -f name=%CONTAINER_NAME% >nul
if not errorlevel 1 (
    echo Stopping and removing existing container...
    docker stop %CONTAINER_NAME%
    docker rm %CONTAINER_NAME%
)

echo Ensuring network exists...
docker network ls | findstr /C:"stock_network" >nul
if errorlevel 1 docker network create stock_network

echo Starting container...
docker run -it --name %CONTAINER_NAME% --network=stock_network %IMAGE_NAME%

pause
