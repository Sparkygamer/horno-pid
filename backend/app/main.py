from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .database import engine, Base
from .routers import recetas, auth, esp32

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Horno PID",
    description="API para gestionar recetas del horno controlado por ESP32",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de la API
app.include_router(auth.router)
app.include_router(recetas.router)
app.include_router(esp32.router)

# Servir el frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
def servir_frontend():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"mensaje": "API del Horno PID funcionando correctamente"}
