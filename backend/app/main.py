from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .database import engine, Base
from .routers import recetas, auth

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Horno PID",
    description="API para gestionar recetas del horno controlado por ESP32",
    version="2.0.0"
)

# Permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(auth.router)
app.include_router(recetas.router)

# Servir el frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def servir_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))