@echo off
:: Titilo de la ventana
title Django Project Setup Script

echo  Iniciando setup del proyecto...
echo.

:: Crear archivo .env
IF NOT EXIST ".env" (
    echo Creando archivo .env predeterminado...

    (
        echo # .env file
        
        echo POSTGRES_USER=usuario
        echo POSTGRES_PASSWORD=passwordsegura
        echo POSTGRES_DB=parchate
        echo POSTGRES_CONTAINER_NAME=postgres_server
        echo POSTGRES_PORT=0811
    ) > ".env"

    echo Archivo .env creado exitosamente.
) ELSE (
    echo Ya existe un archivo .env, no se realizaron cambios.
)



:: Levantamiento de la Base de Datos con Docker Compose
echo Levantando PostgreSQL con Docker Compose...
docker compose up -d

:: Si el anterior comando fallo, intentar con la version antigua
IF %ERRORLEVEL% NEQ 0 (
    echo Intento fallido con 'docker compose', probando con 'docker-compose'...
    docker-compose up -d
)

:: Esperar
echo Cargando...
timeout /t 5 /nobreak > NUL

:: Ejecutar el script SQL de inicialización
:: Asegurarse de que estas variables coincidan con el .env 
set DB_USER=usuario
set DB_NAME=parchate
set CONTAINER_NAME=postgres_server

IF EXIST "Proyecto\Backend\cmd\bd\init.sql" (
    echo Ejecutando script SQL de inicialización...
    type "Proyecto\Backend\cmd\bd\init.sql" | docker exec -i %CONTAINER_NAME% psql -U %DB_USER% -d %DB_NAME%
) ELSE (
    echo No se encontró Proyecto\Backend\cmd\bd\init.sql
)

:: TODO: Descargar dependencias de Python

::Crear y activar entorno virtual

        echo Creando/activando entorno virtual en Proyecto...
        pushd "Proyecto"

        IF NOT EXIST "venv" (
            echo Creando venv con 'python -m venv venv'...
            python -m venv venv
            IF %ERRORLEVEL% NEQ 0 (
                echo Error creando venv con 'python', intentando con 'py -3 -m venv venv'...
                py -3 -m venv venv
            )
        ) ELSE (
            echo Ya existe la carpeta venv, no se creará una nueva.
        )

        echo Activando entorno virtual...
        call venv\Scripts\activate
        call pip install django psycopg2-binary python-dotenv

        popd


echo.

cd ..\..

echo  Setup completado.

:EOF