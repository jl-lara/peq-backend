import json
from fastapi import HTTPException, status, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional

def obtener_panel_productor(db: Session, id_usuario: int):
	# 1. Obtener el id_productor asociado al id_usuario autenticado
	query_productor = text(
		"SELECT id_productor FROM productores WHERE id_usuario = :id_usuario;"
	)
	id_productor = db.execute(query_productor, {"id_usuario": id_usuario}).scalar()

	if not id_productor:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="No se encontró un perfil de productor asociado a este usuario.",
		)

	# 2. Ejecutar la función almacenada fn_obtener_panel_productor
	query_panel = text("SELECT fn_obtener_panel_productor(:p_id_productor);")

	try:
		resultado = db.execute(
			query_panel, {"p_id_productor": id_productor}
		).scalar()
		return resultado
	except Exception as err:
		print(f"Error al ejecutar fn_obtener_panel_productor: {str(err)}")
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error al consultar el panel del productor: {str(err)}",
		)

def obtener_animales_productor(db: Session, id_usuario: int):
	# 1. Buscar el id_productor asociado al id_usuario
	query_prod = text(
		"SELECT id_productor FROM productores WHERE id_usuario = :id_usuario;"
	)
	id_productor = db.execute(query_prod, {"id_usuario": id_usuario}).scalar()

	if not id_productor:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="No se encontró un rancho/productor registrado para este usuario.",
		)

	# 2. Ejecutar la función fn_obtener_animales_productor
	query_animales = text(
		"SELECT fn_obtener_animales_productor(:p_id_productor);"
	)

	try:
		resultado = db.execute(
			query_animales, {"p_id_productor": id_productor}
		).scalar()
		return resultado or []
	except Exception as err:
		print(f"Error al ejecutar fn_obtener_animales_productor: {str(err)}")
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error al obtener los animales del productor: {str(err)}",
		)

def obtener_actividad_productor(db: Session, id_usuario: int):
	query = text("SELECT fn_obtener_actividad_productor(:p_id_usuario);")
	try:
		resultado = db.execute(query, {"p_id_usuario": id_usuario}).scalar()
		return resultado or []
	except Exception as err:
		print(f"Error al ejecutar fn_obtener_actividad_productor: {str(err)}")
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error al consultar el historial de actividad: {str(err)}",
		)