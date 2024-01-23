
# Sistema Automatizado de Inventarios - ANIMAL FOOD

## Descripción

Este proyecto es una API para un sistema automatizado de inventarios de ANIMAL FOOD, desarrollada en Python con FastAPI y una serie de bibliotecas adicionales. Se ha implementado siguiendo los principios de Diseño Guiado por el Dominio (DDD) y Desarrollo Guiado por Pruebas (TDD). La API está contenida en un entorno Docker para facilitar el despliegue y la ejecución.

## Características

- **FastAPI**: Para un desarrollo rápido de endpoints.
- **SQLAlchemy y Alembic**: Para la gestión de la base de datos y migraciones.
- **Pydantic**: Para la validación de datos.
- **Uvicorn**: Como servidor ASGI.
- **Pytest**: Para pruebas.
- **Docker**: Para un despliegue y ejecución sencillos.

## Diagrama ER

![Diagrama ER](URL_DEL_DIAGRAMA)


## Requerimientos

Lista de dependencias del proyecto:
app
fastapi==0.88.0
uvicorn[standard]==0.20.0
pydantic==1.10.4
email-validator==1.3.0
python-multipart==0.0.5
python-dateutil==2.8.2

db
databases[postgresql]==0.7.0
psycopg2-binary==2.9.5
SQLAlchemy==1.4.45
alembic==1.9.1
pytz==2022.7

auth
PyJWT==2.5.0
bcrypt==3.2.0
passlib==1.7.4
cryptography==38.0.1
pycryptodome==3.15.0
sendgrid==6.9.7
jinja2==3.1.2

logging
icecream==2.1.3
loguru==0.6.0

tests
pytest==7.2.0
pytest-asyncio==0.20.3
httpx==0.23.0
asgi-lifespan==2.0.0
requests==2.28.1

lintint
black==23.1.0
isort==5.12.0
mypy==1.1.1


## Despliegue



## Ejecución de Tests




