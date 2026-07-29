"""Adaptador CRUD del modulo comercial sobre la capa existente."""

from sqlalchemy.orm import Session

from app import crud as legacy_crud


def create_productor(db: Session, productor):
	return legacy_crud.create_productor(db=db, productor=productor)


def get_productores(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_usuario: int | None = None,
	nombre: str | None = None,
):
	return legacy_crud.get_productores(
		db=db,
		skip=skip,
		limit=limit,
		id_usuario=id_usuario,
		nombre=nombre,
	)


def update_productor(db: Session, id_productor: int, productor):
	return legacy_crud.update_productor(db=db, id_productor=id_productor, productor=productor)


def delete_productor(db: Session, id_productor: int):
	return legacy_crud.delete_productor(db=db, id_productor=id_productor)


def create_animal(db: Session, animal):
	return legacy_crud.create_animal(db=db, animal=animal)


def get_animales(
	db: Session,
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
):
	return legacy_crud.get_animales(
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


def update_animal(db: Session, id_animal: int, animal):
	return legacy_crud.update_animal(db=db, id_animal=id_animal, animal=animal)


def delete_animal(db: Session, id_animal: int):
	return legacy_crud.delete_animal(db=db, id_animal=id_animal)
