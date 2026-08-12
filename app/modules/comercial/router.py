from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app.database import get_db

from . import crud, schemas

public_router = APIRouter()
router = APIRouter(dependencies=[Depends(auth.get_current_user)])


@router.get("/comercial/productor/", response_model=schemas.ProductorResponse, tags=["Comercial"])
def leer_mi_productor(
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_mi_productor(db=db, id_usuario=current_user.id_usuario)


@router.get("/comercial/animales-productor/", response_model=List[schemas.AnimalRegistradoProductorResponse], tags=["Comercial"])
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


@router.get("/comercial/animales/", response_model=List[schemas.AnimalResponse], tags=["Comercial"])
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


@router.get("/comercial/documentos/", response_model=List[schemas.DocumentoResponse], tags=["Comercial"])
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


@router.get("/comercial/solicitudes/", response_model=List[schemas.SolicitudCertificacionResponse], tags=["Comercial"])
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

@router.get("/comercial/actividades/", response_model=List[schemas.ActividadProductorResponse], tags=["Comercial"])
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

@router.get("/comercial/perfil/", response_model=schemas.ProductorPerfilResponse, tags=["Comercial"])
def leer_perfil_productor(
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_perfil_productor(db=db, id_usuario=current_user.id_usuario)


@router.get("/comercial/documentos-productor/", response_model=List[schemas.DocumentoProductorResponse], tags=["Comercial"])
def leer_documentos_productor(
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_documentos_productor(
		db=db,
		id_usuario=current_user.id_usuario,
	)


@router.get("/comercial/dashboard/", response_model=schemas.DashboardProductorResponse, tags=["Comercial"])
def leer_dashboard_productor(
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_dashboard_productor(
		db=db,
		id_usuario=current_user.id_usuario,
	)


@router.get("/comercial/ficha-tecnica/{arete_id}", response_model=schemas.FichaTecnicaAnimalResponse, tags=["Comercial"])
def leer_ficha_tecnica_animal(
	arete_id: str,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.get_ficha_tecnica_animal(db=db, arete_id=arete_id)


@router.put("/comercial/perfil/cambiar-contrasena/", tags=["Comercial"])
def actualizar_contrasena_productor(
	payload: schemas.CambiarContrasenaRequest,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	# current_user.id_usuario viene directamente de auth.get_current_user
	return crud.cambiar_contrasena_usuario(
		db=db,
		id_usuario=current_user.id_usuario,
		contrasena_actual=payload.contrasena_actual,
		contrasena_nueva=payload.contrasena_nueva,
	)

@router.put("/comercial/perfil/editar/", tags=["Comercial"])
def actualizar_perfil_productor(
	payload: schemas.EditarPerfilProductorRequest,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.editar_perfil_productor(
		db=db,
		id_usuario=current_user.id_usuario,
		nombre=payload.nombre,
		apellido_paterno=payload.apellido_paterno,
		apellido_materno=payload.apellido_materno,
		email=payload.email,
		telefono=payload.telefono,
		ciudad=payload.ciudad,
		nombre_rancho=payload.nombre_rancho,
		direccion=payload.direccion,
		capacidad_animales=payload.capacidad_animales,
		superficie_hectareas=payload.superficie_hectareas,
		documentos=[doc.model_dump() for doc in payload.documentos]
		if payload.documentos
		else [],
	)


@public_router.post(
	"/registro-ranchero-comercial/",
	response_model=schemas.RegistroRancheroComercialDBResponse,
	tags=["Registro Ranchero Comercial"],
)
def registrar_ranchero_comercial_publico(
	registro: schemas.RegistroRancheroComercialDBRequest,
	db: Session = Depends(get_db),
):
	resultado = crud.registrar_ranchero_comercial_db(db=db, registro=registro.model_dump())
	if resultado is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo completar el registro del ranchero comercial")
	return resultado