"""Consultas del modulo traspatio basadas en el usuario autenticado."""

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models


def _get_productor_for_user(db: Session, id_usuario: int) -> models.Productor:
	productor = db.query(models.Productor).filter(models.Productor.id_usuario == id_usuario).first()
	if not productor:
		raise HTTPException(
			status_code=404,
			detail="El usuario autenticado no tiene un perfil de productor asociado.",
		)
	return productor


def get_mi_productor(db: Session, id_usuario: int):
	return _get_productor_for_user(db=db, id_usuario=id_usuario)


def get_mis_animales(
	db: Session,
	id_usuario: int,
	skip: int = 0,
	limit: int = 100,
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
	productor = _get_productor_for_user(db=db, id_usuario=id_usuario)

	query = db.query(models.Animal).filter(models.Animal.id_productor == productor.id_productor)
	if id_raza is not None:
		query = query.filter(models.Animal.id_raza == id_raza)
	if id_estado is not None:
		query = query.filter(models.Animal.id_estado == id_estado)
	if sexo:
		query = query.filter(models.Animal.sexo == sexo.strip().upper())
	if edad_min is not None:
		query = query.filter(models.Animal.edad >= edad_min)
	if edad_max is not None:
		query = query.filter(models.Animal.edad <= edad_max)
	if peso_min is not None:
		query = query.filter(models.Animal.peso_kg >= peso_min)
	if peso_max is not None:
		query = query.filter(models.Animal.peso_kg <= peso_max)
	if arete_id:
		query = query.filter(models.Animal.arete_id == arete_id)
	if proposito_produccion:
		query = query.filter(models.Animal.proposito_produccion == proposito_produccion)

	return query.offset(skip).limit(limit).all()


def get_mis_documentos(
	db: Session,
	id_usuario: int,
	skip: int = 0,
	limit: int = 100,
	id_animal: int | None = None,
	id_estado: int | None = None,
	id_tipo_doc: int | None = None,
	fecha_subida_desde: datetime | None = None,
	fecha_subida_hasta: datetime | None = None,
):
	query = db.query(models.Documento).filter(models.Documento.id_usuario_subio == id_usuario)
	if id_animal is not None:
		query = query.filter(models.Documento.id_animal == id_animal)
	if id_estado is not None:
		query = query.filter(models.Documento.id_estado == id_estado)
	if id_tipo_doc is not None:
		query = query.filter(models.Documento.id_tipo_doc == id_tipo_doc)
	if fecha_subida_desde is not None:
		query = query.filter(models.Documento.fecha_subida >= fecha_subida_desde)
	if fecha_subida_hasta is not None:
		query = query.filter(models.Documento.fecha_subida <= fecha_subida_hasta)

	return query.offset(skip).limit(limit).all()


def get_mis_solicitudes(
	db: Session,
	id_usuario: int,
	skip: int = 0,
	limit: int = 100,
	id_estado: int | None = None,
	id_animal: int | None = None,
	id_veterinario: int | None = None,
	fecha_solicitud_desde: datetime | None = None,
	fecha_solicitud_hasta: datetime | None = None,
):
	productor = _get_productor_for_user(db=db, id_usuario=id_usuario)

	query = (
		db.query(models.SolicitudCertificacion)
		.join(models.Animal, models.SolicitudCertificacion.id_animal == models.Animal.id_animal)
		.filter(models.Animal.id_productor == productor.id_productor)
	)
	if id_estado is not None:
		query = query.filter(models.SolicitudCertificacion.id_estado == id_estado)
	if id_animal is not None:
		query = query.filter(models.SolicitudCertificacion.id_animal == id_animal)
	if id_veterinario is not None:
		query = query.filter(models.SolicitudCertificacion.id_veterinario == id_veterinario)
	if fecha_solicitud_desde is not None:
		query = query.filter(models.SolicitudCertificacion.fecha_solicitud >= fecha_solicitud_desde)
	if fecha_solicitud_hasta is not None:
		query = query.filter(models.SolicitudCertificacion.fecha_solicitud <= fecha_solicitud_hasta)

	return query.offset(skip).limit(limit).all()
