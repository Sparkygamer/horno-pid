from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/recetas", tags=["Recetas"])

@router.get("/", response_model=List[schemas.Receta])
def listar_recetas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_recetas(db, skip=skip, limit=limit)

@router.get("/habilitadas", response_model=List[schemas.Receta])
def listar_recetas_habilitadas(db: Session = Depends(get_db)):
    """Endpoint para la ESP32 / OLED: solo devuelve las recetas habilitadas"""
    return crud.get_recetas_habilitadas(db)

@router.get("/{receta_id}", response_model=schemas.Receta)
def obtener_receta(receta_id: int, db: Session = Depends(get_db)):
    receta = crud.get_receta(db, receta_id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

@router.post("/", response_model=schemas.Receta)
def crear_receta(receta: schemas.RecetaCreate, db: Session = Depends(get_db)):
    return crud.create_receta(db, receta)

@router.put("/{receta_id}", response_model=schemas.Receta)
def actualizar_receta(receta_id: int, receta: schemas.RecetaUpdate, db: Session = Depends(get_db)):
    db_receta = crud.update_receta(db, receta_id, receta)
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return db_receta

@router.delete("/{receta_id}")
def eliminar_receta(receta_id: int, db: Session = Depends(get_db)):
    db_receta = crud.delete_receta(db, receta_id)
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return {"mensaje": "Receta eliminada correctamente"}

@router.post("/{receta_id}/toggle", response_model=schemas.Receta)
def toggle_habilitada(receta_id: int, db: Session = Depends(get_db)):
    """Habilita o deshabilita una receta (para que aparezca o no en la OLED)"""
    db_receta = crud.toggle_habilitada(db, receta_id)
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return db_receta