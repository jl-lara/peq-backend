from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from . import crud, schemas


router = APIRouter()


@router.get(
	"/catalogo-publico/estadisticas-certificacion/",
	response_model=List[schemas.EstadisticaCertificacionResponse],
	tags=["Catálogo Público"],
)
def leer_estadisticas_certificacion(db: Session = Depends(get_db)):
	return crud.get_estadisticas_certificacion(db=db)


@router.get(
	"/catalogo-publico/animales-certificados/",
	response_model=List[schemas.CatalogoAnimalResponse],
	tags=["Catálogo Público"],
)
def leer_catalogo_animales_por_categoria(
	id_categoria: int,
	id_estado: int = 4,
	db: Session = Depends(get_db),
):
	return crud.get_catalogo_animales(db=db, id_categoria=id_categoria, id_estado=id_estado)


@router.get(
	"/catalogo-publico/ficha-tecnica/",
	response_model=schemas.FichaTecnicaQRResponse,
	tags=["Catálogo Público"],
)
def leer_ficha_tecnica_por_arete(
	arete_id: str,
	db: Session = Depends(get_db),
):
	return crud.get_ficha_tecnica_qr(db=db, arete_id=arete_id)
