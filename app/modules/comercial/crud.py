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

def obtener_catalogo_animales(
	db: Session,
	id_categoria: Optional[int] = None,
	id_estado: Optional[int] = None,
):
	query = text(
		"SELECT fn_obtener_catalogo_animales(:p_id_categoria, :p_id_estado);"
	)
	try:
		resultado = db.execute(
			query, {"p_id_categoria": id_categoria, "p_id_estado": id_estado}
		).scalar()
		return resultado or []
	except Exception as err:
		print(f"Error al ejecutar fn_obtener_catalogo_animales: {str(err)}")
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Error al obtener el catálogo de animales.",
		)


def editar_animal_productor(
	db: Session,
	id_animal: int,
	id_usuario: int,
	sexo: str,
	edad: float,
	peso_kg: float,
	condicion_general: str,
	proposito_produccion: str,
	documentos: Optional[list] = None,
):
	# 1. Obtener id_productor
	query_prod = text(
		"SELECT id_productor FROM productores WHERE id_usuario = :id_usuario;"
	)
	id_productor = db.execute(query_prod, {"id_usuario": id_usuario}).scalar()

	if not id_productor:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Productor no encontrado.",
		)

	# 2. Invocación usando CAST para evitar conflicto de ::json en SQLAlchemy
	query_edit = text(
		"""
        SELECT fn_editar_animal(
            :p_id_animal,
            :p_id_productor,
            :p_sexo,
            :p_edad,
            :p_peso_kg,
            :p_condicion_general,
            :p_proposito_produccion,
            CAST(:p_documentos AS JSON)
        );
    """
	)

	documentos_json = json.dumps(documentos) if documentos else json.dumps([])

	try:
		resultado = db.execute(
			query_edit,
			{
				"p_id_animal": id_animal,
				"p_id_productor": id_productor,
				"p_sexo": sexo,
				"p_edad": edad,
				"p_peso_kg": peso_kg,
				"p_condicion_general": condicion_general,
				"p_proposito_produccion": proposito_produccion,
				"p_documentos": documentos_json,
			},
		).scalar()
		db.commit()
		return resultado
	except Exception as err:
		db.rollback()
		print(f"Error al ejecutar fn_editar_animal: {str(err)}")
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"Error al editar animal: {str(err)}",
		)