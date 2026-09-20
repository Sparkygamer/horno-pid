from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..database import get_db
from ..security import obtener_usuario_actual

router = APIRouter(prefix="/recetas", tags=["Recetas"])

@router.get("/", response_model=List[schemas.Receta])
def listar_recetas(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    return crud.get_recetas(db, usuario_id=usuario_actual.id, skip=skip, limit=limit)

@router.get("/habilitadas", response_model=List[schemas.Receta])
def listar_recetas_habilitadas(
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    """Endpoint para la ESP32 / OLED: solo devuelve las recetas habilitadas del panadero"""
    return crud.get_recetas_habilitadas(db, usuario_id=usuario_actual.id)

@router.get("/{receta_id}", response_model=schemas.Receta)
def obtener_receta(
    receta_id: int, 
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    receta = crud.get_receta(db, receta_id, usuario_id=usuario_actual.id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

@router.post("/", response_model=schemas.Receta)
def crear_receta(
    receta: schemas.RecetaCreate, 
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    return crud.create_receta(db, receta, usuario_id=usuario_actual.id)

@router.put("/{receta_id}", response_model=schemas.Receta)
def actualizar_receta(
    receta_id: int, 
    receta: schemas.RecetaUpdate, 
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    db_receta = crud.update_receta(db, receta_id, receta, usuario_id=usuario_actual.id)
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return db_receta

@router.delete("/{receta_id}")
def eliminar_receta(
    receta_id: int, 
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    db_receta = crud.delete_receta(db, receta_id, usuario_id=usuario_actual.id)
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return {"mensaje": "Receta eliminada correctamente"}

@router.post("/{receta_id}/toggle", response_model=schemas.Receta)
def toggle_habilitada(
    receta_id: int, 
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    """Habilita o deshabilita una receta (para que aparezca o no en la OLED)"""
    db_receta = crud.toggle_habilitada(db, receta_id, usuario_id=usuario_actual.id)
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return db_receta