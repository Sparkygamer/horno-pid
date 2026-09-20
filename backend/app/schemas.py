from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ========== USUARIO ==========
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Usuario(UsuarioBase):
    id: int
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True

# ========== RECETA ==========
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
    usuario_id: int
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    class Config:
        from_attributes = True

# ========== TOKEN ==========
class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: Usuario