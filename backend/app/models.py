from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tiempo_horneado = Column(Integer, nullable=False)      # minutos
    temperatura = Column(Float, nullable=False)            # grados °C
    habilitada = Column(Boolean, default=False)            # si aparece en la OLED
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())