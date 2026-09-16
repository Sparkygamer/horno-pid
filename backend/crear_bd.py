from app.database import engine, Base
from app import models

print("Creando la base de datos y las tablas...")
Base.metadata.create_all(bind=engine)
print("¡Base de datos creada correctamente!")