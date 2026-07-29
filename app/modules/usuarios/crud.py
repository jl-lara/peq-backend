"""Adaptador CRUD del modulo de usuarios sobre la capa existente."""

from sqlalchemy.orm import Session

from app import crud as legacy_crud


def create_rol(db: Session, rol):
    return legacy_crud.create_rol(db=db, rol=rol)


def get_roles(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
    return legacy_crud.get_roles(db=db, skip=skip, limit=limit, nombre=nombre)


def update_rol(db: Session, id_rol: int, rol):
    return legacy_crud.update_rol(db=db, id_rol=id_rol, rol=rol)


def delete_rol(db: Session, id_rol: int):
    return legacy_crud.delete_rol(db=db, id_rol=id_rol)


def create_usuario(db: Session, usuario):
    return legacy_crud.create_usuario(db=db, usuario=usuario)


def get_usuarios(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_rol: int | None = None,
    id_estado: int | None = None,
    ciudad: str | None = None,
    usuario: str | None = None,
    email: str | None = None,
):
    return legacy_crud.get_usuarios(
        db=db,
        skip=skip,
        limit=limit,
        id_rol=id_rol,
        id_estado=id_estado,
        ciudad=ciudad,
        usuario=usuario,
        email=email,
    )


def update_usuario(db: Session, id_usuario: int, usuario):
    return legacy_crud.update_usuario(db=db, id_usuario=id_usuario, usuario=usuario)


def delete_usuario(db: Session, id_usuario: int):
    return legacy_crud.delete_usuario(db=db, id_usuario=id_usuario)


def authenticate_user(db: Session, username: str, password: str):
    return legacy_crud.authenticate_user(db=db, username=username, password=password)
