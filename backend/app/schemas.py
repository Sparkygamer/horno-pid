from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecetaBase(BaseModel):
    nombre: str
    tiempo_horneado: int
    temperatura: float

class RecetaCreate(RecetaBase):
    pass

class RecetaUpdate(BaseModel):
    nombre: Optional[str] = None
    tiempo_horneado: Optional[int] = None
    temperatura: Optional[float] = None
    habilitada: Optional[bool] = None

class Receta(RecetaBase):
    id: int
    habilitada: bool
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    class Config:
        from_attributes = True