from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app import auth
from app.database import get_db

from . import crud, schemas

router = APIRouter(dependencies=[Depends(auth.get_current_user)])


@router.get(
	"/comercial/dashboard/",
	response_model=schemas.PanelProductorResponse,
	tags=["Comercial"],
)
def obtener_dashboard_comercial(
	db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)
):
	return crud.obtener_panel_productor(db=db, id_usuario=current_user.id_usuario)

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