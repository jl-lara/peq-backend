"""Adaptador CRUD del modulo catalogos_base sobre la capa existente."""

from sqlalchemy.orm import Session

from app import crud as legacy_crud


def create_estado(db: Session, estado):
    return legacy_crud.create_estado(db=db, estado=estado)


def get_estados(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
    return legacy_crud.get_estados(db=db, skip=skip, limit=limit, nombre=nombre)


def update_estado(db: Session, id_estado: int, estado):
    return legacy_crud.update_estado(db=db, id_estado=id_estado, estado=estado)


def delete_estado(db: Session, id_estado: int):
    return legacy_crud.delete_estado(db=db, id_estado=id_estado)


def create_accion(db: Session, accion):
    return legacy_crud.create_accion(db=db, accion=accion)


def get_acciones(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
    return legacy_crud.get_acciones(db=db, skip=skip, limit=limit, nombre=nombre)


def update_accion(db: Session, id_accion: int, accion):
    return legacy_crud.update_accion(db=db, id_accion=id_accion, accion=accion)


def delete_accion(db: Session, id_accion: int):
    return legacy_crud.delete_accion(db=db, id_accion=id_accion)
