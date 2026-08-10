from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

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