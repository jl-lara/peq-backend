"""Adaptador CRUD del modulo admin sobre la capa existente."""

from datetime import datetime

from sqlalchemy.orm import Session

from app import crud as legacy_crud


def create_tipo_doc(db: Session, tipo_doc):
	return legacy_crud.create_tipo_doc(db=db, tipo_doc=tipo_doc)


def get_tipos_doc(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
	return legacy_crud.get_tipos_doc(db=db, skip=skip, limit=limit, nombre=nombre)


def update_tipo_doc(db: Session, id_tipo_doc: int, tipo_doc):
	return legacy_crud.update_tipo_doc(db=db, id_tipo_doc=id_tipo_doc, tipo_doc=tipo_doc)


def delete_tipo_doc(db: Session, id_tipo_doc: int):
	return legacy_crud.delete_tipo_doc(db=db, id_tipo_doc=id_tipo_doc)


def create_requisito_doc(db: Session, requisito):
	return legacy_crud.create_requisito_doc(db=db, requisito=requisito)


def get_requisitos_docs(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_rol: int | None = None,
	id_tipo_doc: int | None = None,
	obligatorio: bool | None = None,
):
	return legacy_crud.get_requisitos_docs(
		db=db,
		skip=skip,
		limit=limit,
		id_rol=id_rol,
		id_tipo_doc=id_tipo_doc,
		obligatorio=obligatorio,
	)


def update_requisito_doc(db: Session, id_rol: int, id_tipo_doc: int, requisito):
	return legacy_crud.update_requisito_doc(
		db=db,
		id_rol=id_rol,
		id_tipo_doc=id_tipo_doc,
		requisito=requisito,
	)


def delete_requisito_doc(db: Session, id_rol: int, id_tipo_doc: int):
	return legacy_crud.delete_requisito_doc(db=db, id_rol=id_rol, id_tipo_doc=id_tipo_doc)


def create_documento(db: Session, documento):
	return legacy_crud.create_documento(db=db, documento=documento)


def get_documentos(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_usuario_subio: int | None = None,
	id_validador: int | None = None,
	id_estado: int | None = None,
	id_tipo_doc: int | None = None,
	fecha_subida_desde: datetime | None = None,
	fecha_subida_hasta: datetime | None = None,
):
	return legacy_crud.get_documentos(
		db=db,
		skip=skip,
		limit=limit,
		id_usuario_subio=id_usuario_subio,
		id_validador=id_validador,
		id_estado=id_estado,
		id_tipo_doc=id_tipo_doc,
		fecha_subida_desde=fecha_subida_desde,
		fecha_subida_hasta=fecha_subida_hasta,
	)


def update_documento(db: Session, id_doc_animal: int, documento):
	return legacy_crud.update_documento(db=db, id_doc_animal=id_doc_animal, documento=documento)


def delete_documento(db: Session, id_doc_animal: int):
	return legacy_crud.delete_documento(db=db, id_doc_animal=id_doc_animal)


def create_categoria(db: Session, categoria):
	return legacy_crud.create_categoria(db=db, categoria=categoria)


def get_categorias(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
	return legacy_crud.get_categorias(db=db, skip=skip, limit=limit, nombre=nombre)


def update_categoria(db: Session, id_categoria: int, categoria):
	return legacy_crud.update_categoria(db=db, id_categoria=id_categoria, categoria=categoria)


def delete_categoria(db: Session, id_categoria: int):
	return legacy_crud.delete_categoria(db=db, id_categoria=id_categoria)


def create_raza(db: Session, raza):
	return legacy_crud.create_raza(db=db, raza=raza)


def get_razas(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_categoria: int | None = None,
	nombre: str | None = None,
):
	return legacy_crud.get_razas(
		db=db,
		skip=skip,
		limit=limit,
		id_categoria=id_categoria,
		nombre=nombre,
	)


def update_raza(db: Session, id_raza: int, raza):
	return legacy_crud.update_raza(db=db, id_raza=id_raza, raza=raza)


def delete_raza(db: Session, id_raza: int):
	return legacy_crud.delete_raza(db=db, id_raza=id_raza)


def create_precio(db: Session, precio):
	return legacy_crud.create_precio(db=db, precio=precio)


def get_precios(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_categoria: int | None = None,
	activo: bool | None = None,
	fecha_vigencia_desde: datetime | None = None,
	fecha_vigencia_hasta: datetime | None = None,
):
	return legacy_crud.get_precios(
		db=db,
		skip=skip,
		limit=limit,
		id_categoria=id_categoria,
		activo=activo,
		fecha_vigencia_desde=fecha_vigencia_desde,
		fecha_vigencia_hasta=fecha_vigencia_hasta,
	)


def update_precio(db: Session, id_precio: int, precio):
	return legacy_crud.update_precio(db=db, id_precio=id_precio, precio=precio)


def delete_precio(db: Session, id_precio: int):
	return legacy_crud.delete_precio(db=db, id_precio=id_precio)


def create_precio_animal(db: Session, precio_animal):
	return legacy_crud.create_precio_animal(db=db, precio_animal=precio_animal)


def get_precios_animales(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_precio: int | None = None,
	id_animal: int | None = None,
	fecha_calculo_desde: datetime | None = None,
	fecha_calculo_hasta: datetime | None = None,
):
	return legacy_crud.get_precios_animales(
		db=db,
		skip=skip,
		limit=limit,
		id_precio=id_precio,
		id_animal=id_animal,
		fecha_calculo_desde=fecha_calculo_desde,
		fecha_calculo_hasta=fecha_calculo_hasta,
	)


def update_precio_animal(db: Session, id_precio: int, id_animal: int, precio_animal):
	return legacy_crud.update_precio_animal(
		db=db,
		id_precio=id_precio,
		id_animal=id_animal,
		precio_animal=precio_animal,
	)


def delete_precio_animal(db: Session, id_precio: int, id_animal: int):
	return legacy_crud.delete_precio_animal(db=db, id_precio=id_precio, id_animal=id_animal)


def create_bitacora(db: Session, bitacora):
	return legacy_crud.create_bitacora(db=db, bitacora=bitacora)


def get_bitacoras(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_usuario: int | None = None,
	id_accion: int | None = None,
	tabla_afectada: str | None = None,
	fecha_cambio_desde: datetime | None = None,
	fecha_cambio_hasta: datetime | None = None,
):
	return legacy_crud.get_bitacoras(
		db=db,
		skip=skip,
		limit=limit,
		id_usuario=id_usuario,
		id_accion=id_accion,
		tabla_afectada=tabla_afectada,
		fecha_cambio_desde=fecha_cambio_desde,
		fecha_cambio_hasta=fecha_cambio_hasta,
	)


def update_bitacora(db: Session, id_bitacora: int, bitacora):
	return legacy_crud.update_bitacora(db=db, id_bitacora=id_bitacora, bitacora=bitacora)


def delete_bitacora(db: Session, id_bitacora: int):
	return legacy_crud.delete_bitacora(db=db, id_bitacora=id_bitacora)


def create_enfermedad(db: Session, enfermedad):
	return legacy_crud.create_enfermedad(db=db, enfermedad=enfermedad)


def get_enfermedades(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	nombre: str | None = None,
	requiere_cuarentena: bool | None = None,
):
	return legacy_crud.get_enfermedades(
		db=db,
		skip=skip,
		limit=limit,
		nombre=nombre,
		requiere_cuarentena=requiere_cuarentena,
	)


def update_enfermedad(db: Session, id_enfermedad: int, enfermedad):
	return legacy_crud.update_enfermedad(db=db, id_enfermedad=id_enfermedad, enfermedad=enfermedad)


def delete_enfermedad(db: Session, id_enfermedad: int):
	return legacy_crud.delete_enfermedad(db=db, id_enfermedad=id_enfermedad)


def create_enfermedad_animal(db: Session, enfermedad_animal):
	return legacy_crud.create_enfermedad_animal(db=db, enfermedad_animal=enfermedad_animal)


def get_enfermedades_animales(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_enfermedad: int | None = None,
	id_animal: int | None = None,
	estado: str | None = None,
	fecha_deteccion_desde: datetime | None = None,
	fecha_deteccion_hasta: datetime | None = None,
):
	return legacy_crud.get_enfermedades_animales(
		db=db,
		skip=skip,
		limit=limit,
		id_enfermedad=id_enfermedad,
		id_animal=id_animal,
		estado=estado,
		fecha_deteccion_desde=fecha_deteccion_desde,
		fecha_deteccion_hasta=fecha_deteccion_hasta,
	)


def update_enfermedad_animal(db: Session, id_enfermedad: int, id_animal: int, enfermedad_animal):
	return legacy_crud.update_enfermedad_animal(
		db=db,
		id_enfermedad=id_enfermedad,
		id_animal=id_animal,
		enfermedad_animal=enfermedad_animal,
	)


def delete_enfermedad_animal(db: Session, id_enfermedad: int, id_animal: int):
	return legacy_crud.delete_enfermedad_animal(db=db, id_enfermedad=id_enfermedad, id_animal=id_animal)
