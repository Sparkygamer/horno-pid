from sqlalchemy.orm import Session
from . import models, schemas

def get_recetas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Receta).offset(skip).limit(limit).all()

def get_receta(db: Session, receta_id: int):
    return db.query(models.Receta).filter(models.Receta.id == receta_id).first()

def get_receta_activa(db: Session):
    return db.query(models.Receta).filter(models.Receta.activa == True).first()

def create_receta(db: Session, receta: schemas.RecetaCreate):
    db_receta = models.Receta(**receta.model_dump())
    db.add(db_receta)
    db.commit()
    db.refresh(db_receta)
    return db_receta

def update_receta(db: Session, receta_id: int, receta: schemas.RecetaUpdate):
    db_receta = get_receta(db, receta_id)
    if not db_receta:
        return None

    update_data = receta.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_receta, key, value)

    db.commit()
    db.refresh(db_receta)
    return db_receta

def delete_receta(db: Session, receta_id: int):
    db_receta = get_receta(db, receta_id)
    if not db_receta:
        return None
    db.delete(db_receta)
    db.commit()
    return db_receta

def activar_receta(db: Session, receta_id: int):
    # Desactivar todas las recetas
    db.query(models.Receta).update({models.Receta.activa: False})
    
    # Activar la receta seleccionada
    db_receta = get_receta(db, receta_id)
    if db_receta:
        db_receta.activa = True
        db.commit()
        db.refresh(db_receta)
    return db_receta