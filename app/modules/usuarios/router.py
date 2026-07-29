from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app.database import get_db

from . import crud, schemas

public_router = APIRouter()
protected_router = APIRouter(dependencies=[Depends(auth.get_current_user)])


@protected_router.post("/roles/", response_model=schemas.RolResponse, tags=["Catálogos - Roles"])
def crear_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    return crud.create_rol(db=db, rol=rol)


@protected_router.get("/roles/", response_model=List[schemas.RolResponse], tags=["Catálogos - Roles"])
def leer_roles(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
    return crud.get_roles(db=db, skip=skip, limit=limit, nombre=nombre)


@protected_router.put("/roles/{id_rol}", response_model=schemas.RolResponse, tags=["Catálogos - Roles"])
def actualizar_rol(id_rol: int, rol: schemas.RolCreate, db: Session = Depends(get_db)):
    return crud.update_rol(db=db, id_rol=id_rol, rol=rol)


@protected_router.delete("/roles/{id_rol}", tags=["Catálogos - Roles"])
def eliminar_rol(id_rol: int, db: Session = Depends(get_db)):
    return crud.delete_rol(db=db, id_rol=id_rol)


@protected_router.post("/usuarios/", response_model=schemas.UsuarioResponse, tags=["Usuarios"])
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)


@protected_router.get("/usuarios/", response_model=List[schemas.UsuarioResponse], tags=["Usuarios"])
def leer_usuarios(
    skip: int = 0,
    limit: int = 100,
    id_rol: int | None = None,
    id_estado: int | None = None,
    ciudad: str | None = None,
    usuario: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_usuarios(
        db=db,
        skip=skip,
        limit=limit,
        id_rol=id_rol,
        id_estado=id_estado,
        ciudad=ciudad,
        usuario=usuario,
        email=email,
    )


@protected_router.put("/usuarios/{id_usuario}", response_model=schemas.UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario(id_usuario: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.update_usuario(db=db, id_usuario=id_usuario, usuario=usuario)


@protected_router.delete("/usuarios/{id_usuario}", tags=["Usuarios"])
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return crud.delete_usuario(db=db, id_usuario=id_usuario)


@public_router.post("/login", response_model=schemas.Token, tags=["Autenticación"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.usuario})
    return {"access_token": access_token, "token_type": "bearer"}
