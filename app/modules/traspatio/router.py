from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app.database import get_db

from . import crud, schemas

router = APIRouter(dependencies=[Depends(auth.get_current_user)])


@router.get("/traspatio/productor/", response_model=schemas.ProductorResponse, tags=["Traspatio"])
def leer_mi_productor(
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_mi_productor(db=db, id_usuario=current_user.id_usuario)


@router.get("/traspatio/animales-productor/", response_model=List[schemas.AnimalRegistradoProductorResponse], tags=["Traspatio"])
def leer_animales_productor(
	skip: int = 0,
	limit: int = 100,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_animales_productor(
		db=db,
		id_usuario=current_user.id_usuario,
		skip=skip,
		limit=limit,
	)


@router.get("/traspatio/animales/", response_model=List[schemas.AnimalResponse], tags=["Traspatio"])
def leer_mis_animales(
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
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_mis_animales(
		db=db,
		id_usuario=current_user.id_usuario,
		skip=skip,
		limit=limit,
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


@router.get("/traspatio/documentos/", response_model=List[schemas.DocumentoResponse], tags=["Traspatio"])
def leer_mis_documentos(
	skip: int = 0,
	limit: int = 100,
	id_estado: int | None = None,
	id_tipo_doc: int | None = None,
	fecha_subida_desde: datetime | None = None,
	fecha_subida_hasta: datetime | None = None,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_mis_documentos(
		db=db,
		id_usuario=current_user.id_usuario,
		skip=skip,
		limit=limit,
		id_estado=id_estado,
		id_tipo_doc=id_tipo_doc,
		fecha_subida_desde=fecha_subida_desde,
		fecha_subida_hasta=fecha_subida_hasta,
	)


@router.get("/traspatio/solicitudes/", response_model=List[schemas.SolicitudCertificacionResponse], tags=["Traspatio"])
def leer_mis_solicitudes(
	skip: int = 0,
	limit: int = 100,
	id_estado: int | None = None,
	id_animal: int | None = None,
	id_veterinario: int | None = None,
	fecha_solicitud_desde: datetime | None = None,
	fecha_solicitud_hasta: datetime | None = None,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_mis_solicitudes(
		db=db,
		id_usuario=current_user.id_usuario,
		skip=skip,
		limit=limit,
		id_estado=id_estado,
		id_animal=id_animal,
		id_veterinario=id_veterinario,
		fecha_solicitud_desde=fecha_solicitud_desde,
		fecha_solicitud_hasta=fecha_solicitud_hasta,
	)

@router.get("/traspatio/actividades/", response_model=List[schemas.ActividadProductorResponse], tags=["Traspatio"])
def leer_mis_actividades(
	skip: int = 0,
	limit: int = 100,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_mis_actividades(
		db=db,
		id_usuario=current_user.id_usuario,
		skip=skip,
		limit=limit,
	)

@router.get("/traspatio/perfil/", response_model=schemas.ProductorPerfilResponse, tags=["Traspatio"])
def leer_perfil_productor(
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_perfil_productor(db=db, id_usuario=current_user.id_usuario)


@router.get("/traspatio/documentos-productor/", response_model=List[schemas.DocumentoProductorResponse], tags=["Traspatio"])
def leer_documentos_productor(
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_documentos_productor(
		db=db,
		id_usuario=current_user.id_usuario,
	)


@router.get("/traspatio/dashboard/", response_model=schemas.DashboardProductorResponse, tags=["Traspatio"])
def leer_dashboard_productor(
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_dashboard_productor(
		db=db,
		id_usuario=current_user.id_usuario,
	)


@router.get("/traspatio/ficha-tecnica/{arete_id}", response_model=schemas.FichaTecnicaAnimalResponse, tags=["Traspatio"])
def leer_ficha_tecnica_animal(
	arete_id: str,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_ficha_tecnica_animal(db=db, arete_id=arete_id)