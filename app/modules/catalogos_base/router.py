from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app.database import get_db

from . import crud, schemas

router = APIRouter(dependencies=[Depends(auth.get_current_user)])


@router.post("/estados/", response_model=schemas.EstadoResponse, tags=["Catálogos - Estados"])
def crear_estado(estado: schemas.EstadoCreate, db: Session = Depends(get_db)):
    return crud.create_estado(db=db, estado=estado)


@router.get("/estados/", response_model=List[schemas.EstadoResponse], tags=["Catálogos - Estados"])
def leer_estados(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
    return crud.get_estados(db=db, skip=skip, limit=limit, nombre=nombre)


@router.put("/estados/{id_estado}", response_model=schemas.EstadoResponse, tags=["Catálogos - Estados"])
def actualizar_estado(id_estado: int, estado: schemas.EstadoCreate, db: Session = Depends(get_db)):
    return crud.update_estado(db=db, id_estado=id_estado, estado=estado)


@router.delete("/estados/{id_estado}", tags=["Catálogos - Estados"])
def eliminar_estado(id_estado: int, db: Session = Depends(get_db)):
    return crud.delete_estado(db=db, id_estado=id_estado)


@router.post("/acciones/", response_model=schemas.AccionResponse, tags=["Auditoría"])
def crear_accion(accion: schemas.AccionCreate, db: Session = Depends(get_db)):
    return crud.create_accion(db=db, accion=accion)


@router.get("/acciones/", response_model=List[schemas.AccionResponse], tags=["Auditoría"])
def leer_acciones(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
    return crud.get_acciones(db=db, skip=skip, limit=limit, nombre=nombre)


@router.put("/acciones/{id_accion}", response_model=schemas.AccionResponse, tags=["Auditoría"])
def actualizar_accion(id_accion: int, accion: schemas.AccionCreate, db: Session = Depends(get_db)):
    return crud.update_accion(db=db, id_accion=id_accion, accion=accion)


@router.delete("/acciones/{id_accion}", tags=["Auditoría"])
def eliminar_accion(id_accion: int, db: Session = Depends(get_db)):
    return crud.delete_accion(db=db, id_accion=id_accion)
