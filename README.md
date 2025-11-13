# Bibliobus APP

Aplicación que carga el dataset “Casa de Cultura” en PostgreSQL, expone un backend FastAPI con arquitectura de tres capas y sirve un front muy ligero (HTML+JS) para catálogo, recomendaciones, dashboard de KPIs y registro de valoraciones.

## 1. Requisitos previos

- Docker y Docker Compose (para la base de datos)
- Python 3.11+ (para API/ETL)
- `pip` / entornos virtuales

```
proyecto-app/
├── db/                # Postgres y scripts SQL
├── data/raw/          # CSV originales y limpios
├── etl/               # Script de carga masiva opcional
└── api/               # FastAPI + frontend estático
```

## 2. Base de datos

1. Situarse en `proyecto-app/db`
2. Arrancar Postgres:
   ```
   docker compose up -d
   ```
3. Crear esquema limpio (borra y recrea `lib.*`):
   ```
   Get-Content -Raw 01_schema.sql | docker exec -i bibliobus_db psql -U app -d libdb
   ```
4. Editar `02_load_data.sql` y dejar descomentados los CSV deseados:
   - `book_mkp.csv`, `copies_mkp.csv`, etc. → dataset completo (~10k libros)
   - o bien `books_clean_1.csv` + `copies_clean_1.csv` si se filtra la info
   - Revisa que `SET datestyle TO 'DMY';` esté al inicio si hay fechas `dd/mm/yyyy`
5. Cargar datos:
   ```
   Get-Content -Raw 02_load_data.sql | docker exec -i bibliobus_db psql -U app -d libdb
   ```
6. Validar conteos y huérfanos:
   ```
   Get-Content -Raw 03_checks.sql | docker exec -i bibliobus_db psql -U app -d libdb
   ```

## 3. API + Frontend

1. `cd proyecto-app/api`
2. Crear entorno virtual e instalar dependencias:
   ```
   python -m venv .venv
   .venv\Scripts\activate   # en Windows (usar source .venv/bin/activate en Unix)
   pip install -r requirements.txt
   ```
3. Ejecutar FastAPI:
   ```
   uvicorn app.main:app --reload
   ```
4. Secciones disponibles en el navegador:
   - `http://127.0.0.1:8000/catalog` → catálogo filtrable
   - `http://127.0.0.1:8000/book?id=123` → detalle del libro
   - `http://127.0.0.1:8000/recommendations` → recomendaciones “a priori”
   - `http://127.0.0.1:8000/dashboard` → KPIs
   - `http://127.0.0.1:8000/ratings` → formulario de valoraciones

Los endpoints REST viven en `/api/...` (`/api/books`, `/api/ratings`, etc.) y tienen Swagger en `/docs`.

## 4. Tests rápidos

Desde `proyecto-app/api`:
```
pytest
```
(usa SQLite en memoria)

## 5. Notas

- Los CSV “clean” deben contener IDs consistentes: si se reduce el catálogo, limpiar también `copies_clean_1.csv` y `ratings_clean_1.csv`.
- `02_load_data.sql` incluye bloques comentados para cargar una versión u otra del dataset.
- El script `etl/carga.py` (opcional) muestra cómo automatizar validaciones y cargas con pandas/psycopg.
- Cuando se cambie la fuente de datos, repetir `01_schema.sql` + `02_load_data.sql`.

Con esto cualquier compañero puede levantar la BD, cargar los CSV apropiados y ejecutar la app en local. ¡Listo para subir a GitHub!***