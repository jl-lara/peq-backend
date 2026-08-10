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

def _get_productor_for_user(db: Session, id_usuario: int) -> models.Productor:
	productor = db.query(models.Productor).filter(models.Productor.id_usuario == id_usuario).first()
	if not productor:
		raise HTTPException(
			status_code=404,
			detail="El usuario autenticado no tiene un perfil de productor asociado.",
		)
	return productor



def get_mi_productor(db: Session, id_usuario: int):
	return _get_productor_for_user(db=db, id_usuario=id_usuario)


def get_animales_productor(db: Session, id_usuario: int, skip: int = 0, limit: int = 100):
	productor = _get_productor_for_user(db=db, id_usuario=id_usuario)

	rows = (
		db.query(
			models.Animal.id_animal,
			models.Animal.arete_id,
			models.CategoriaGanado.nombre.label("tipo_animal"),
			models.Raza.nombre.label("raza"),
			models.Animal.edad.label("edad_anios"),
			models.Animal.peso_kg,
			models.Estado.nombre.label("estado_certificacion"),
			func.coalesce(models.PrecioAnimal.precio_final, 0).label("precio_estimado"),
			models.Animal.fecha_registro,
		)
		.join(models.Raza, models.Animal.id_raza == models.Raza.id_raza)
		.join(models.CategoriaGanado, models.Raza.id_categoria == models.CategoriaGanado.id_categoria)
		.join(models.Estado, models.Animal.id_estado == models.Estado.id_estado)
		.outerjoin(models.PrecioAnimal, models.Animal.id_animal == models.PrecioAnimal.id_animal)
		.filter(models.Animal.id_productor == productor.id_productor)
		.order_by(models.Animal.fecha_registro.desc())
		.offset(skip)
		.limit(limit)
		.all()
	)

	return [
		{
			"id_animal": row.id_animal,
			"arete_id": row.arete_id,
			"tipo_animal": row.tipo_animal,
			"raza": row.raza,
			"edad_anios": row.edad_anios,
			"peso_kg": row.peso_kg,
			"estado_certificacion": row.estado_certificacion,
			"precio_estimado": float(row.precio_estimado or 0),
			"fecha_registro": row.fecha_registro,
		}
		for row in rows
	]


def get_mis_animales(
	db: Session,
	id_usuario: int,
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
):
	productor = _get_productor_for_user(db=db, id_usuario=id_usuario)

	query = db.query(models.Animal).filter(models.Animal.id_productor == productor.id_productor)
	if id_raza is not None:
		query = query.filter(models.Animal.id_raza == id_raza)
	if id_estado is not None:
		query = query.filter(models.Animal.id_estado == id_estado)
	if sexo:
		query = query.filter(models.Animal.sexo == sexo.strip().upper())
	if edad_min is not None:
		query = query.filter(models.Animal.edad >= edad_min)
	if edad_max is not None:
		query = query.filter(models.Animal.edad <= edad_max)
	if peso_min is not None:
		query = query.filter(models.Animal.peso_kg >= peso_min)
	if peso_max is not None:
		query = query.filter(models.Animal.peso_kg <= peso_max)
	if arete_id:
		query = query.filter(models.Animal.arete_id == arete_id)
	if proposito_produccion:
		query = query.filter(models.Animal.proposito_produccion == proposito_produccion)

	return query.offset(skip).limit(limit).all()
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