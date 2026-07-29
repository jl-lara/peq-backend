"""Adaptador CRUD del modulo veterinario sobre la capa existente."""

from datetime import datetime

from sqlalchemy.orm import Session

from app import crud as legacy_crud


def create_veterinario(db: Session, veterinario):
	return legacy_crud.create_veterinario(db=db, veterinario=veterinario)


def get_veterinarios(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_usuario: int | None = None,
	cedula_profesional: str | None = None,
	especialidad: str | None = None,
):
	return legacy_crud.get_veterinarios(
		db=db,
		skip=skip,
		limit=limit,
		id_usuario=id_usuario,
		cedula_profesional=cedula_profesional,
		especialidad=especialidad,
	)


def update_veterinario(db: Session, id_docs_vet: int, veterinario):
	return legacy_crud.update_veterinario(db=db, id_docs_vet=id_docs_vet, veterinario=veterinario)


def delete_veterinario(db: Session, id_docs_vet: int):
	return legacy_crud.delete_veterinario(db=db, id_docs_vet=id_docs_vet)


def create_solicitud(db: Session, solicitud):
	return legacy_crud.create_solicitud(db=db, solicitud=solicitud)


def get_solicitudes(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_estado: int | None = None,
	id_animal: int | None = None,
	id_veterinario: int | None = None,
	fecha_solicitud_desde: datetime | None = None,
	fecha_solicitud_hasta: datetime | None = None,
):
	return legacy_crud.get_solicitudes(
		db=db,
		skip=skip,
		limit=limit,
		id_estado=id_estado,
		id_animal=id_animal,
		id_veterinario=id_veterinario,
		fecha_solicitud_desde=fecha_solicitud_desde,
		fecha_solicitud_hasta=fecha_solicitud_hasta,
	)


def update_solicitud(db: Session, id_solicitud: int, solicitud):
	return legacy_crud.update_solicitud(db=db, id_solicitud=id_solicitud, solicitud=solicitud)


def delete_solicitud(db: Session, id_solicitud: int):
	return legacy_crud.delete_solicitud(db=db, id_solicitud=id_solicitud)


def create_certificacion(db: Session, certificacion):
	return legacy_crud.create_certificacion(db=db, certificacion=certificacion)


def get_certificaciones(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_solicitud: int | None = None,
	dictamen: str | None = None,
	fecha_certificacion_desde: datetime | None = None,
	fecha_certificacion_hasta: datetime | None = None,
):
	return legacy_crud.get_certificaciones(
		db=db,
		skip=skip,
		limit=limit,
		id_solicitud=id_solicitud,
		dictamen=dictamen,
		fecha_certificacion_desde=fecha_certificacion_desde,
		fecha_certificacion_hasta=fecha_certificacion_hasta,
	)


def update_certificacion(db: Session, id_certificacion: int, certificacion):
	return legacy_crud.update_certificacion(
		db=db,
		id_certificacion=id_certificacion,
		certificacion=certificacion,
	)


def delete_certificacion(db: Session, id_certificacion: int):
	return legacy_crud.delete_certificacion(db=db, id_certificacion=id_certificacion)
