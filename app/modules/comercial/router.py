from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app.database import get_db

from . import crud, schemas

router = APIRouter(dependencies=[Depends(auth.get_current_user)])


@router.post("/productores/", response_model=schemas.ProductorResponse, tags=["Productores"])
def crear_productor(productor: schemas.ProductorCreate, db: Session = Depends(get_db)):
	return crud.create_productor(db=db, productor=productor)


@router.get("/productores/", response_model=List[schemas.ProductorResponse], tags=["Productores"])
def leer_productores(
	skip: int = 0,
	limit: int = 100,
	id_usuario: int | None = None,
	nombre: str | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_productores(
		db=db,
		skip=skip,
		limit=limit,
		id_usuario=id_usuario,
		nombre=nombre,
	)


@router.put("/productores/{id_productor}", response_model=schemas.ProductorResponse, tags=["Productores"])
def actualizar_productor(id_productor: int, productor: schemas.ProductorCreate, db: Session = Depends(get_db)):
	return crud.update_productor(db=db, id_productor=id_productor, productor=productor)


@router.delete("/productores/{id_productor}", tags=["Productores"])
def eliminar_productor(id_productor: int, db: Session = Depends(get_db)):
	return crud.delete_productor(db=db, id_productor=id_productor)


@router.post("/animales/", response_model=schemas.AnimalResponse, tags=["Animales"])
def crear_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
	return crud.create_animal(db=db, animal=animal)


@router.get("/animales/", response_model=List[schemas.AnimalResponse], tags=["Animales"])
def leer_animales(
	skip: int = 0,
	limit: int = 100,
	id_productor: int | None = None,
	id_raza: int | None = None,
	id_estado: int | None = None,
	sexo: str | None = None,
	edad_min: int | None = None,
	edad_max: int | None = None,
	peso_min: float | None = None,
	peso_max: float | None = None,
	arete_id: str | None = None,
	proposito_produccion: str | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_animales(
		db=db,
		skip=skip,
		limit=limit,
		id_productor=id_productor,
		id_raza=id_raza,
		id_estado=id_estado,
		sexo=sexo,
		edad_min=edad_min,
		edad_max=edad_max,
		peso_min=peso_min,
		peso_max=peso_max,
		arete_id=arete_id,
		proposito_produccion=proposito_produccion,
	)


@router.put("/animales/{id_animal}", response_model=schemas.AnimalResponse, tags=["Animales"])
def actualizar_animal(id_animal: int, animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
	return crud.update_animal(db=db, id_animal=id_animal, animal=animal)


@router.delete("/animales/{id_animal}", tags=["Animales"])
def eliminar_animal(id_animal: int, db: Session = Depends(get_db)):
	return crud.delete_animal(db=db, id_animal=id_animal)
