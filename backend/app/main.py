from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import recetas

# Crear las tablas (por si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Horno PID",
    description="API para gestionar recetas del horno controlado por ESP32",
    version="1.0.0"
)

# Permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de recetas
app.include_router(recetas.router)

@app.get("/")
def root():
    return {"mensaje": "API del Horno PID funcionando correctamente"}