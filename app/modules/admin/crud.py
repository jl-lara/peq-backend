"""Adaptador CRUD del modulo admin sobre la capa existente."""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import crud as legacy_crud
from app import models


def create_tipo_doc(db: Session, tipo_doc):
	return legacy_crud.create_tipo_doc(db=db, tipo_doc=tipo_doc)


def get_tipos_doc(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
	return legacy_crud.get_tipos_doc(db=db, skip=skip, limit=limit, nombre=nombre)


def update_tipo_doc(db: Session, id_tipo_doc: int, tipo_doc):
	return legacy_crud.update_tipo_doc(db=db, id_tipo_doc=id_tipo_doc, tipo_doc=tipo_doc)


def delete_tipo_doc(db: Session, id_tipo_doc: int):
	return legacy_crud.delete_tipo_doc(db=db, id_tipo_doc=id_tipo_doc)


def create_estado(db: Session, estado):
	return legacy_crud.create_estado(db=db, estado=estado)


def get_estados(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
	return legacy_crud.get_estados(db=db, skip=skip, limit=limit, nombre=nombre)


def update_estado(db: Session, id_estado: int, estado):
	return legacy_crud.update_estado(db=db, id_estado=id_estado, estado=estado)


def delete_estado(db: Session, id_estado: int):
	return legacy_crud.delete_estado(db=db, id_estado=id_estado)


def create_rol(db: Session, rol):
	return legacy_crud.create_rol(db=db, rol=rol)


def get_roles(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
	return legacy_crud.get_roles(db=db, skip=skip, limit=limit, nombre=nombre)


def update_rol(db: Session, id_rol: int, rol):
	return legacy_crud.update_rol(db=db, id_rol=id_rol, rol=rol)


def delete_rol(db: Session, id_rol: int):
	return legacy_crud.delete_rol(db=db, id_rol=id_rol)


def create_accion(db: Session, accion):
	return legacy_crud.create_accion(db=db, accion=accion)


def get_acciones(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
	return legacy_crud.get_acciones(db=db, skip=skip, limit=limit, nombre=nombre)


def update_accion(db: Session, id_accion: int, accion):
	return legacy_crud.update_accion(db=db, id_accion=id_accion, accion=accion)


def delete_accion(db: Session, id_accion: int):
	return legacy_crud.delete_accion(db=db, id_accion=id_accion)


def create_requisito_doc(db: Session, requisito):
	return legacy_crud.create_requisito_doc(db=db, requisito=requisito)


def create_usuario(db: Session, usuario):
	return legacy_crud.create_usuario(db=db, usuario=usuario)


def get_usuarios(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_rol: int | None = None,
	id_estado: int | None = None,
	ciudad: str | None = None,
	usuario: str | None = None,
	email: str | None = None,
):
	return legacy_crud.get_usuarios(
		db=db,
		skip=skip,
		limit=limit,
		id_rol=id_rol,
		id_estado=id_estado,
		ciudad=ciudad,
		usuario=usuario,
		email=email,
	)


def update_usuario(db: Session, id_usuario: int, usuario):
	return legacy_crud.update_usuario(db=db, id_usuario=id_usuario, usuario=usuario)


def delete_usuario(db: Session, id_usuario: int):
	return legacy_crud.delete_usuario(db=db, id_usuario=id_usuario)


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


def create_solicitud_cambio(db: Session, solicitud_cambio):
	return legacy_crud.create_solicitud_cambio(db=db, solicitud_cambio=solicitud_cambio)


def get_solicitudes_cambio(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_usuario_solicita: int | None = None,
	id_usuario_objetivo: int | None = None,
	id_revisor: int | None = None,
	id_estado: int | None = None,
	campo_afectado: str | None = None,
	fecha_solicitud_desde: datetime | None = None,
	fecha_solicitud_hasta: datetime | None = None,
):
	return legacy_crud.get_solicitudes_cambio(
		db=db,
		skip=skip,
		limit=limit,
		id_usuario_solicita=id_usuario_solicita,
		id_usuario_objetivo=id_usuario_objetivo,
		id_revisor=id_revisor,
		id_estado=id_estado,
		campo_afectado=campo_afectado,
		fecha_solicitud_desde=fecha_solicitud_desde,
		fecha_solicitud_hasta=fecha_solicitud_hasta,
	)


def update_solicitud_cambio(db: Session, id_solicitud_cambio: int, solicitud_cambio):
	return legacy_crud.update_solicitud_cambio(
		db=db,
		id_solicitud_cambio=id_solicitud_cambio,
		solicitud_cambio=solicitud_cambio,
	)


def delete_solicitud_cambio(db: Session, id_solicitud_cambio: int):
	return legacy_crud.delete_solicitud_cambio(db=db, id_solicitud_cambio=id_solicitud_cambio)


def get_documentos(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_animal: int | None = None,
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
		id_animal=id_animal,
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


def get_resumen_usuarios_activos_por_tipo(db: Session):
	rows = (
		db.query(
			models.Rol.nombre.label("tipo_usuario"),
			func.count(models.Usuario.id_usuario).label("total_usuarios_activos"),
		)
		.join(models.Usuario, models.Usuario.id_rol == models.Rol.id_rol)
		.join(models.Estado, models.Usuario.id_estado == models.Estado.id_estado)
		.filter(func.upper(models.Estado.nombre) == "ACTIVO")
		.group_by(models.Rol.nombre)
		.order_by(models.Rol.nombre)
		.all()
	)
	return [
		{
			"tipo_usuario": row.tipo_usuario,
			"total_usuarios_activos": row.total_usuarios_activos,
		}
		for row in rows
	]


def get_solicitudes_registro_admin(
	db: Session,
	id_estado: int | None = None,
	id_rol: int | None = None,
):
	query = (
		db.query(
			models.Usuario.id_usuario,
			models.Usuario.nombre,
			models.Usuario.apellido_paterno,
			models.Usuario.telefono,
			models.Usuario.email,
			models.Usuario.fecha_registro,
			models.Rol.nombre.label("tipo_rol"),
			models.Estado.nombre.label("estado_usuario"),
		)
		.join(models.Rol, models.Usuario.id_rol == models.Rol.id_rol)
		.join(models.Estado, models.Usuario.id_estado == models.Estado.id_estado)
	)
	if id_estado is not None:
		query = query.filter(models.Usuario.id_estado == id_estado)
	if id_rol is not None:
		query = query.filter(models.Usuario.id_rol == id_rol)

	rows = query.order_by(models.Usuario.fecha_registro.desc()).all()
	return [
		{
			"id_usuario": row.id_usuario,
			"id_usuario_display": f"USR-{row.id_usuario:03d}",
			"nombre_completo": f"{row.nombre} {row.apellido_paterno}",
			"tipo_rol": row.tipo_rol,
			"email": row.email,
			"telefono": row.telefono,
			"fecha_solicitud": row.fecha_registro,
			"estado_usuario": row.estado_usuario,
		}
		for row in rows
	]


def get_bitacora_admin(
	db: Session,
	id_usuario: int | None = None,
	id_rol: int | None = None,
	tabla_afectada: str | None = None,
	fecha_cambio_desde: datetime | None = None,
	fecha_cambio_hasta: datetime | None = None,
):
	query = (
		db.query(
			models.Bitacora.fecha_cambio,
			models.Usuario.nombre,
			models.Usuario.apellido_paterno,
			models.Usuario.ciudad,
			models.Rol.nombre.label("tipo_usuario"),
			models.Accion.nombre.label("accion"),
			models.Bitacora.tabla_afectada,
			models.Bitacora.valor_anterior,
			models.Bitacora.valor_nuevo,
		)
		.join(models.Usuario, models.Bitacora.id_usuario == models.Usuario.id_usuario)
		.join(models.Rol, models.Usuario.id_rol == models.Rol.id_rol)
		.join(models.Accion, models.Bitacora.id_accion == models.Accion.id_accion)
	)
	if id_usuario is not None:
		query = query.filter(models.Bitacora.id_usuario == id_usuario)
	if id_rol is not None:
		query = query.filter(models.Usuario.id_rol == id_rol)
	if tabla_afectada:
		query = query.filter(models.Bitacora.tabla_afectada == tabla_afectada)
	if fecha_cambio_desde is not None:
		query = query.filter(models.Bitacora.fecha_cambio >= fecha_cambio_desde)
	if fecha_cambio_hasta is not None:
		query = query.filter(models.Bitacora.fecha_cambio <= fecha_cambio_hasta)

	rows = query.order_by(models.Bitacora.fecha_cambio.desc()).all()
	return [
		{
			"fecha_hora": row.fecha_cambio,
			"usuario_responsable": f"{row.nombre} {row.apellido_paterno}",
			"tipo_usuario": row.tipo_usuario,
			"accion": row.accion,
			"entidad": row.tabla_afectada,
			"detalles": f"Registro afectado: {row.valor_nuevo or row.valor_anterior or ''}",
			"ciudad": row.ciudad,
		}
		for row in rows
	]


def get_documentos_revision_admin(
	db: Session,
	id_animal: int | None = None,
	id_usuario_subio: int | None = None,
	id_validador: int | None = None,
	id_estado: int | None = None,
	id_tipo_doc: int | None = None,
	fecha_subida_desde: datetime | None = None,
	fecha_subida_hasta: datetime | None = None,
):
	query = (
		db.query(
			models.Documento.id_doc_animal,
			models.Documento.id_animal,
			models.Documento.id_usuario_subio,
			models.TipoDoc.nombre.label("tipo_documento"),
			models.Documento.url_archivo,
			models.Estado.nombre.label("estado_revision"),
			models.Documento.notas,
			models.Documento.fecha_revision,
		)
		.join(models.TipoDoc, models.Documento.id_tipo_doc == models.TipoDoc.id_tipo_doc)
		.join(models.Estado, models.Documento.id_estado == models.Estado.id_estado)
	)
	if id_animal is not None:
		query = query.filter(models.Documento.id_animal == id_animal)
	if id_usuario_subio is not None:
		query = query.filter(models.Documento.id_usuario_subio == id_usuario_subio)
	if id_validador is not None:
		query = query.filter(models.Documento.id_validador == id_validador)
	if id_estado is not None:
		query = query.filter(models.Documento.id_estado == id_estado)
	if id_tipo_doc is not None:
		query = query.filter(models.Documento.id_tipo_doc == id_tipo_doc)
	if fecha_subida_desde is not None:
		query = query.filter(models.Documento.fecha_subida >= fecha_subida_desde)
	if fecha_subida_hasta is not None:
		query = query.filter(models.Documento.fecha_subida <= fecha_subida_hasta)

	rows = query.order_by(models.Documento.fecha_subida.desc()).all()
	return [
		{
			"id_doc_animal": row.id_doc_animal,
			"id_animal": row.id_animal,
			"id_usuario_subio": row.id_usuario_subio,
			"tipo_documento": row.tipo_documento,
			"enlace_documento": row.url_archivo,
			"estado_revision": row.estado_revision,
			"notas_administrador": row.notas,
			"fecha_revision": row.fecha_revision,
		}
		for row in rows
	]


def get_perfil_administrador(db: Session, usuario_actual: models.Usuario):
	perfil = (
		db.query(
			models.Usuario.id_usuario,
			models.Usuario.nombre,
			models.Usuario.apellido_paterno,
			models.Usuario.apellido_materno,
			models.Usuario.email,
			models.Usuario.telefono,
			models.Usuario.ciudad,
			models.Usuario.fecha_registro,
			models.Rol.nombre.label("rol_sistema"),
			models.Estado.nombre.label("estatus_cuenta"),
		)
		.join(models.Rol, models.Usuario.id_rol == models.Rol.id_rol)
		.join(models.Estado, models.Usuario.id_estado == models.Estado.id_estado)
		.filter(models.Usuario.id_usuario == usuario_actual.id_usuario)
		.first()
	)
	if not perfil:
		return None

	nombre_completo = f"{perfil.nombre} {perfil.apellido_paterno}"
	if perfil.apellido_materno:
		nombre_completo = f"{nombre_completo} {perfil.apellido_materno}"

	return {
		"id_usuario": perfil.id_usuario,
		"nombre_completo": nombre_completo,
		"email": perfil.email,
		"telefono": perfil.telefono,
		"ciudad": perfil.ciudad,
		"rol_sistema": perfil.rol_sistema,
		"miembro_desde": perfil.fecha_registro,
		"estatus_cuenta": perfil.estatus_cuenta,
	}
