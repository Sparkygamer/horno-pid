from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import recetas, auth, esp32  # ← agregar esp32

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

app.include_router(auth.router)
app.include_router(recetas.router)
app.include_router(esp32.router)  # ← agregar esta línea


@app.get("/")
def root():
    return {"mensaje": "API del Horno PID funcionando correctamente"}
