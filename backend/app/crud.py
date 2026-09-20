from sqlalchemy.orm import Session
from . import models, schemas

def get_recetas(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Receta).filter(models.Receta.usuario_id == usuario_id).offset(skip).limit(limit).all()

def get_receta(db: Session, receta_id: int, usuario_id: int):
    return db.query(models.Receta).filter(
        models.Receta.id == receta_id,
        models.Receta.usuario_id == usuario_id
    ).first()

def get_recetas_habilitadas(db: Session, usuario_id: int):
    return db.query(models.Receta).filter(
        models.Receta.usuario_id == usuario_id,
        models.Receta.habilitada == True
    ).all()

def create_receta(db: Session, receta: schemas.RecetaCreate, usuario_id: int):
    db_receta = models.Receta(**receta.model_dump(), usuario_id=usuario_id)
    db.add(db_receta)
    db.commit()
    db.refresh(db_receta)
    return db_receta

def update_receta(db: Session, receta_id: int, receta: schemas.RecetaUpdate, usuario_id: int):
    db_receta = get_receta(db, receta_id, usuario_id)
    if not db_receta:
        return None

    update_data = receta.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_receta, key, value)

    db.commit()
    db.refresh(db_receta)
    return db_receta

def delete_receta(db: Session, receta_id: int, usuario_id: int):
    db_receta = get_receta(db, receta_id, usuario_id)
    if not db_receta:
        return None
    db.delete(db_receta)
    db.commit()
    return db_receta

def toggle_habilitada(db: Session, receta_id: int, usuario_id: int):
    db_receta = get_receta(db, receta_id, usuario_id)
    if not db_receta:
        return None
    
    db_receta.habilitada = not db_receta.habilitada
    db.commit()
    db.refresh(db_receta)
    return db_receta