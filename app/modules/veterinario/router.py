from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app.database import get_db

from . import crud, schemas

router = APIRouter(dependencies=[Depends(auth.get_current_user)])


@router.post("/veterinarios/", response_model=schemas.DatosVeterinariosResponse, tags=["Flujo Certificación"])
def crear_veterinario(veterinario: schemas.DatosVeterinariosCreate, db: Session = Depends(get_db)):
	return crud.create_veterinario(db=db, veterinario=veterinario)


@router.get("/veterinarios/", response_model=List[schemas.DatosVeterinariosResponse], tags=["Flujo Certificación"])
def leer_veterinarios(
	skip: int = 0,
	limit: int = 100,
	id_usuario: int | None = None,
	cedula_profesional: str | None = None,
	especialidad: str | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_veterinarios(
		db=db,
		skip=skip,
		limit=limit,
		id_usuario=id_usuario,
		cedula_profesional=cedula_profesional,
		especialidad=especialidad,
	)


@router.put("/veterinarios/{id_docs_vet}", response_model=schemas.DatosVeterinariosResponse, tags=["Flujo Certificación"])
def actualizar_veterinario(
	id_docs_vet: int,
	veterinario: schemas.DatosVeterinariosCreate,
	db: Session = Depends(get_db),
):
	return crud.update_veterinario(db=db, id_docs_vet=id_docs_vet, veterinario=veterinario)


@router.delete("/veterinarios/{id_docs_vet}", tags=["Flujo Certificación"])
def eliminar_veterinario(id_docs_vet: int, db: Session = Depends(get_db)):
	return crud.delete_veterinario(db=db, id_docs_vet=id_docs_vet)


@router.post("/solicitudes/", response_model=schemas.SolicitudCertificacionResponse, tags=["Flujo Certificación"])
def crear_solicitud(solicitud: schemas.SolicitudCertificacionCreate, db: Session = Depends(get_db)):
	return crud.create_solicitud(db=db, solicitud=solicitud)


@router.get("/solicitudes/", response_model=List[schemas.SolicitudCertificacionResponse], tags=["Flujo Certificación"])
def leer_solicitudes(
	skip: int = 0,
	limit: int = 100,
	id_estado: int | None = None,
	id_animal: int | None = None,
	id_veterinario: int | None = None,
	fecha_solicitud_desde: datetime | None = None,
	fecha_solicitud_hasta: datetime | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_solicitudes(
		db=db,
		skip=skip,
		limit=limit,
		id_estado=id_estado,
		id_animal=id_animal,
		id_veterinario=id_veterinario,
		fecha_solicitud_desde=fecha_solicitud_desde,
		fecha_solicitud_hasta=fecha_solicitud_hasta,
	)


@router.put("/solicitudes/{id_solicitud}", response_model=schemas.SolicitudCertificacionResponse, tags=["Flujo Certificación"])
def actualizar_solicitud(
	id_solicitud: int,
	solicitud: schemas.SolicitudCertificacionCreate,
	db: Session = Depends(get_db),
):
	return crud.update_solicitud(db=db, id_solicitud=id_solicitud, solicitud=solicitud)


@router.delete("/solicitudes/{id_solicitud}", tags=["Flujo Certificación"])
def eliminar_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
	return crud.delete_solicitud(db=db, id_solicitud=id_solicitud)


@router.post("/certificaciones/", response_model=schemas.CertificacionResponse, tags=["Flujo Certificación"])
def crear_certificacion(certificacion: schemas.CertificacionCreate, db: Session = Depends(get_db)):
	return crud.create_certificacion(db=db, certificacion=certificacion)


@router.get("/certificaciones/", response_model=List[schemas.CertificacionResponse], tags=["Flujo Certificación"])
def leer_certificaciones(
	skip: int = 0,
	limit: int = 100,
	id_solicitud: int | None = None,
	dictamen: str | None = None,
	fecha_certificacion_desde: datetime | None = None,
	fecha_certificacion_hasta: datetime | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_certificaciones(
		db=db,
		skip=skip,
		limit=limit,
		id_solicitud=id_solicitud,
		dictamen=dictamen,
		fecha_certificacion_desde=fecha_certificacion_desde,
		fecha_certificacion_hasta=fecha_certificacion_hasta,
	)


@router.put("/certificaciones/{id_certificacion}", response_model=schemas.CertificacionResponse, tags=["Flujo Certificación"])
def actualizar_certificacion(
	id_certificacion: int,
	certificacion: schemas.CertificacionCreate,
	db: Session = Depends(get_db),
):
	return crud.update_certificacion(
		db=db,
		id_certificacion=id_certificacion,
		certificacion=certificacion,
	)


@router.delete("/certificaciones/{id_certificacion}", tags=["Flujo Certificación"])
def eliminar_certificacion(id_certificacion: int, db: Session = Depends(get_db)):
	return crud.delete_certificacion(db=db, id_certificacion=id_certificacion)
