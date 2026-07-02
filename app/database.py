import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv # Necesitas instalar python-dotenv

load_dotenv() # Carga las variables del archivo .env

# Lee la URL de forma segura
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()