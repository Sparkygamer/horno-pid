from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/esp32", tags=["ESP32"])

# Clave para la ESP32
ESP32_API_KEY = "horno_pid_esp32_2026"


def verificar_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != ESP32_API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")
    return True


@router.get("/recetas/{usuario_id}", response_model=List[schemas.Receta])
def obtener_recetas_habilitadas_esp32(
    usuario_id: int, db: Session = Depends(get_db), _: bool = Depends(verificar_api_key)
):
    """
    Devuelve las recetas habilitadas de un panadero.
    Header: X-API-Key: horno_pid_esp32_2026
    """
    recetas = crud.get_recetas_habilitadas(db, usuario_id=usuario_id)
    return recetas


@router.get("/recetas/{usuario_id}/resumen")
def obtener_resumen_esp32(
    usuario_id: int, db: Session = Depends(get_db), _: bool = Depends(verificar_api_key)
):
    """
    Versión ligera para la OLED.
    """
    recetas = crud.get_recetas_habilitadas(db, usuario_id=usuario_id)

    return {
        "total": len(recetas),
        "recetas": [
            {
                "id": r.id,
                "nombre": r.nombre,
                "tiempo": r.tiempo_horneado,
                "temperatura": r.temperatura,
            }
            for r in recetas
        ],
    }
