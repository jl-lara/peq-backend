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

@router.get("/comercial/animales/", tags=["Comercial/Traspatio"])
def listar_animales(
	id_categoria: Optional[int] = None,
	id_estado: Optional[int] = None,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.obtener_catalogo_animales(
		db=db, id_categoria=id_categoria, id_estado=id_estado
	)


@router.put("/comercial/animales/{id_animal}/editar/", tags=["Comercial/Traspatio"])
def actualizar_animal(
	id_animal: int,
	payload: schemas.EditarAnimalRequest,
	db: Session = Depends(get_db),
	current_user=Depends(auth.get_current_user),
):
	return crud.editar_animal_productor(
		db=db,
		id_animal=id_animal,
		id_usuario=current_user.id_usuario,
		sexo=payload.sexo,
		edad=payload.edad,
		peso_kg=payload.peso_kg,
		condicion_general=payload.condicion_general,
		proposito_produccion=payload.proposito_produccion,
		documentos=[doc.model_dump() for doc in payload.documentos]
		if payload.documentos
		else [],
	)