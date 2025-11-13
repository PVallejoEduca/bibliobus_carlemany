from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .routers import books, kpis, ratings, recs

app = FastAPI(title="Bibliobus API", version="1.0.0")

API_PREFIX = "/api"

app.include_router(books.router, prefix=API_PREFIX)
app.include_router(ratings.router, prefix=API_PREFIX)
app.include_router(recs.router, prefix=API_PREFIX)
app.include_router(kpis.router, prefix=API_PREFIX)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def serve_page(name: str):
    return FileResponse(static_dir / name)


@app.get("/", include_in_schema=False)
@app.get("/catalog", include_in_schema=False)
def catalog_page():
    """Catálogo como página principal."""
    return serve_page("catalog.html")


@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return serve_page("dashboard.html")


@app.get("/recommendations", include_in_schema=False)
def recommendations_page():
    return serve_page("recommendations.html")


@app.get("/ratings", include_in_schema=False)
def ratings_page():
    return serve_page("ratings.html")


@app.get("/book", include_in_schema=False)
def book_page():
    return serve_page("book.html")
