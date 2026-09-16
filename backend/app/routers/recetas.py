from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/recetas", tags=["Recetas"])

@router.get("/", response_model=List[schemas.Receta])
def listar_recetas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_recetas(db, skip=skip, limit=limit)

@router.get("/activa", response_model=schemas.Receta)
def obtener_receta_activa(db: Session = Depends(get_db)):
    receta = crud.get_receta_activa(db)
    if not receta:
        raise HTTPException(status_code=404, detail="No hay receta activa")
    return receta

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

@router.post("/{receta_id}/activar", response_model=schemas.Receta)
def activar_receta(receta_id: int, db: Session = Depends(get_db)):
    db_receta = crud.activar_receta(db, receta_id)
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return db_receta