from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app import models
from app.database import get_db

from . import crud, schemas



def require_veterinario_user(current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
	rol = db.query(models.Rol).filter(models.Rol.id_rol == current_user.id_rol).first()
	if rol is None or rol.nombre.strip().upper() != "VETERINARIO":
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="No tienes permisos para acceder al panel de veterinario",
		)
	return current_user


router = APIRouter(dependencies=[Depends(require_veterinario_user)])


@router.get("/perfil/", response_model=schemas.PerfilVeterinarioResponse, tags=["Panel Veterinario"])
def leer_perfil_veterinario(current_user=Depends(require_veterinario_user), db: Session = Depends(get_db)):
	perfil = crud.get_perfil_veterinario(db=db, id_usuario=current_user.id_usuario)
	if perfil is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el perfil del veterinario autenticado")
	return perfil


@router.get(
	"/perfil-detallado/",
	response_model=schemas.PerfilVeterinarioDetalladoResponse,
	response_model_exclude_none=True,
	tags=["Panel Veterinario"],
)
def leer_perfil_veterinario_detallado(current_user=Depends(require_veterinario_user), db: Session = Depends(get_db)):
	perfil = crud.get_perfil_veterinario_detallado(db=db, id_usuario=current_user.id_usuario)
	if perfil is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el perfil detallado del veterinario autenticado")
	return perfil


@router.put(
	"/perfil-actualizar-db/",
	response_model=schemas.PerfilVeterinarioActualizarDBResponse,
	tags=["Panel Veterinario"],
)
def actualizar_perfil_veterinario_db(
	perfil: schemas.PerfilVeterinarioActualizarDBRequest,
	current_user=Depends(require_veterinario_user),
	db: Session = Depends(get_db),
):
	resultado = crud.update_perfil_veterinario_db(db=db, id_usuario=current_user.id_usuario, perfil=perfil.model_dump())
	if resultado is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo actualizar el perfil del veterinario autenticado")
	return resultado


@router.put(
	"/revision-certificacion-db/",
	response_model=schemas.RevisionCertificacionVeterinariaDBResponse,
	tags=["Panel Veterinario"],
)
def registrar_revision_certificacion_db(
	revision: schemas.RevisionCertificacionVeterinariaDBRequest,
	current_user=Depends(require_veterinario_user),
	db: Session = Depends(get_db),
):
	resultado = crud.registrar_revision_veterinaria_db(db=db, revision=revision.model_dump())
	if resultado is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo registrar la revisión de la certificación")
	return resultado


@router.get("/solicitudes-panel/", response_model=List[schemas.SolicitudPanelVeterinarioResponse], tags=["Panel Veterinario"])
def leer_solicitudes_panel(
	id_estado: int | None = None,
	current_user=Depends(require_veterinario_user),
	db: Session = Depends(get_db),
):
	return crud.get_solicitudes_panel_vet(db=db, id_veterinario=current_user.id_usuario, id_estado=id_estado)


@router.get(
	"/solicitudes-panel-db/",
	response_model=List[schemas.SolicitudPanelVeterinarioDBResponse],
	tags=["Panel Veterinario"],
)
def leer_solicitudes_panel_db(
	id_estado: int | None = None,
	current_user=Depends(require_veterinario_user),
	db: Session = Depends(get_db),
):
	return crud.get_solicitudes_panel_vet_db(db=db, id_veterinario=current_user.id_usuario, id_estado=id_estado)


@router.get("/bitacora/", response_model=List[schemas.BitacoraVeterinarioResponse], tags=["Panel Veterinario"])
def leer_bitacora_veterinario(current_user=Depends(require_veterinario_user), db: Session = Depends(get_db)):
	return crud.get_bitacora_vet(db=db, id_usuario=current_user.id_usuario)


@router.get(
	"/bitacora-db/",
	response_model=List[schemas.BitacoraVeterinarioDBResponse],
	tags=["Panel Veterinario"],
)
def leer_bitacora_veterinario_db(current_user=Depends(require_veterinario_user), db: Session = Depends(get_db)):
	return crud.get_bitacora_vet_db(db=db, id_usuario=current_user.id_usuario)


@router.get("/documentos-subidos/", response_model=List[schemas.DocumentoVeterinarioResponse], tags=["Panel Veterinario"])
def leer_documentos_subidos(current_user=Depends(require_veterinario_user), db: Session = Depends(get_db)):
	return crud.get_documentos_vet(db=db, id_usuario=current_user.id_usuario)


@router.get(
	"/documentos-subidos-db/",
	response_model=List[schemas.DocumentoVeterinarioDBResponse],
	tags=["Panel Veterinario"],
)
def leer_documentos_subidos_db(current_user=Depends(require_veterinario_user), db: Session = Depends(get_db)):
	return crud.get_documentos_vet_db(db=db, id_usuario=current_user.id_usuario)


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
