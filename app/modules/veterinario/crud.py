"""Adaptador CRUD del modulo veterinario sobre la capa existente."""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import crud as legacy_crud
from app import models


def create_veterinario(db: Session, veterinario):
	return legacy_crud.create_veterinario(db=db, veterinario=veterinario)


def get_veterinarios(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_usuario: int | None = None,
	cedula_profesional: str | None = None,
	especialidad: str | None = None,
):
	return legacy_crud.get_veterinarios(
		db=db,
		skip=skip,
		limit=limit,
		id_usuario=id_usuario,
		cedula_profesional=cedula_profesional,
		especialidad=especialidad,
	)


def update_veterinario(db: Session, id_docs_vet: int, veterinario):
	return legacy_crud.update_veterinario(db=db, id_docs_vet=id_docs_vet, veterinario=veterinario)


def delete_veterinario(db: Session, id_docs_vet: int):
	return legacy_crud.delete_veterinario(db=db, id_docs_vet=id_docs_vet)


def create_solicitud(db: Session, solicitud):
	return legacy_crud.create_solicitud(db=db, solicitud=solicitud)


def get_solicitudes(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_estado: int | None = None,
	id_animal: int | None = None,
	id_veterinario: int | None = None,
	fecha_solicitud_desde: datetime | None = None,
	fecha_solicitud_hasta: datetime | None = None,
):
	return legacy_crud.get_solicitudes(
		db=db,
		skip=skip,
		limit=limit,
		id_estado=id_estado,
		id_animal=id_animal,
		id_veterinario=id_veterinario,
		fecha_solicitud_desde=fecha_solicitud_desde,
		fecha_solicitud_hasta=fecha_solicitud_hasta,
	)


def update_solicitud(db: Session, id_solicitud: int, solicitud):
	return legacy_crud.update_solicitud(db=db, id_solicitud=id_solicitud, solicitud=solicitud)


def delete_solicitud(db: Session, id_solicitud: int):
	return legacy_crud.delete_solicitud(db=db, id_solicitud=id_solicitud)


def create_certificacion(db: Session, certificacion):
	return legacy_crud.create_certificacion(db=db, certificacion=certificacion)


def get_certificaciones(
	db: Session,
	skip: int = 0,
	limit: int = 100,
	id_solicitud: int | None = None,
	dictamen: str | None = None,
	fecha_certificacion_desde: datetime | None = None,
	fecha_certificacion_hasta: datetime | None = None,
):
	return legacy_crud.get_certificaciones(
		db=db,
		skip=skip,
		limit=limit,
		id_solicitud=id_solicitud,
		dictamen=dictamen,
		fecha_certificacion_desde=fecha_certificacion_desde,
		fecha_certificacion_hasta=fecha_certificacion_hasta,
	)


def update_certificacion(db: Session, id_certificacion: int, certificacion):
	return legacy_crud.update_certificacion(
		db=db,
		id_certificacion=id_certificacion,
		certificacion=certificacion,
	)


def delete_certificacion(db: Session, id_certificacion: int):
	return legacy_crud.delete_certificacion(db=db, id_certificacion=id_certificacion)


def get_perfil_veterinario(db: Session, id_usuario: int):
	perfil = (
		db.query(
			models.Usuario.nombre,
			models.Usuario.apellido_paterno,
			models.Usuario.apellido_materno,
			models.Usuario.email,
			models.Usuario.telefono,
			models.Usuario.ciudad,
			models.Estado.nombre.label("estado_usuario"),
			models.Usuario.fecha_registro,
			models.DatosVeterinarios.cedula_profesional,
			models.DatosVeterinarios.especialidad,
			models.DatosVeterinarios.universidad,
			func.count(models.SolicitudCertificacion.id_solicitud).label("total_certificaciones"),
		)
		.join(models.Estado, models.Usuario.id_estado == models.Estado.id_estado)
		.join(models.DatosVeterinarios, models.Usuario.id_usuario == models.DatosVeterinarios.id_usuario)
		.outerjoin(
			models.SolicitudCertificacion,
			(models.SolicitudCertificacion.id_veterinario == models.Usuario.id_usuario)
			& (models.SolicitudCertificacion.id_estado == 4),
		)
		.filter(models.Usuario.id_usuario == id_usuario)
		.group_by(
			models.Usuario.nombre,
			models.Usuario.apellido_paterno,
			models.Usuario.apellido_materno,
			models.Usuario.email,
			models.Usuario.telefono,
			models.Usuario.ciudad,
			models.Estado.nombre,
			models.Usuario.fecha_registro,
			models.DatosVeterinarios.cedula_profesional,
			models.DatosVeterinarios.especialidad,
			models.DatosVeterinarios.universidad,
		)
		.first()
	)
	if not perfil:
		return None

	nombre_completo = f"{perfil.nombre} {perfil.apellido_paterno}"
	if perfil.apellido_materno:
		nombre_completo = f"{nombre_completo} {perfil.apellido_materno}"

	return {
		"nombre_completo": nombre_completo,
		"email": perfil.email,
		"telefono": perfil.telefono,
		"ciudad": perfil.ciudad,
		"estado_usuario": perfil.estado_usuario,
		"fecha_registro": perfil.fecha_registro,
		"cedula_profesional": perfil.cedula_profesional,
		"especialidad": perfil.especialidad,
		"universidad": perfil.universidad,
		"total_certificaciones": int(perfil.total_certificaciones or 0),
	}


def get_solicitudes_panel_vet(
	db: Session,
	id_veterinario: int,
	id_estado: int | None = None,
):
	query = (
		db.query(
			models.SolicitudCertificacion.id_solicitud,
			models.SolicitudCertificacion.fecha_solicitud,
			models.SolicitudCertificacion.id_estado,
			models.Animal.arete_id,
			models.CategoriaGanado.nombre.label("tipo_ganado"),
			models.Productor.nombre.label("rancho"),
			models.Usuario.nombre.label("nombre_productor_nombre"),
			models.Usuario.apellido_paterno.label("nombre_productor_apellido"),
			models.Raza.nombre.label("raza"),
			models.Animal.edad,
			models.Animal.peso_kg,
			models.Estado.nombre.label("estado_solicitud"),
		)
		.join(models.Animal, models.SolicitudCertificacion.id_animal == models.Animal.id_animal)
		.join(models.Productor, models.Animal.id_productor == models.Productor.id_productor)
		.join(models.Usuario, models.Productor.id_usuario == models.Usuario.id_usuario)
		.join(models.Raza, models.Animal.id_raza == models.Raza.id_raza)
		.join(models.CategoriaGanado, models.Raza.id_categoria == models.CategoriaGanado.id_categoria)
		.join(models.Estado, models.SolicitudCertificacion.id_estado == models.Estado.id_estado)
		.filter(models.SolicitudCertificacion.id_veterinario == id_veterinario)
	)
	if id_estado is not None:
		query = query.filter(models.SolicitudCertificacion.id_estado == id_estado)

	rows = query.order_by(models.SolicitudCertificacion.fecha_solicitud.desc()).all()
	return [
		{
			"codigo_solicitud": f"SOL-{row.id_solicitud:03d}",
			"id_solicitud": row.id_solicitud,
			"arete_animal": row.arete_id,
			"tipo_ganado": row.tipo_ganado,
			"nombre_productor": f"{row.nombre_productor_nombre} {row.nombre_productor_apellido}",
			"rancho": row.rancho,
			"raza": row.raza,
			"edad_anios": row.edad,
			"peso_est_kg": row.peso_kg,
			"fecha_solicitud": row.fecha_solicitud,
			"estado_solicitud": row.estado_solicitud,
		}
		for row in rows
	]


def get_bitacora_vet(db: Session, id_usuario: int):
	rows = (
		db.query(
			models.Bitacora.fecha_cambio,
			models.Accion.nombre.label("tipo_accion"),
			models.Bitacora.tabla_afectada,
			models.Bitacora.valor_anterior,
			models.Bitacora.valor_nuevo,
		)
		.join(models.Accion, models.Bitacora.id_accion == models.Accion.id_accion)
		.filter(models.Bitacora.id_usuario == id_usuario)
		.order_by(models.Bitacora.fecha_cambio.desc())
		.all()
	)
	return [
		{
			"fecha_hora": row.fecha_cambio,
			"tipo_accion": row.tipo_accion,
			"entidad_afectada": row.tabla_afectada,
			"detalles": f"ID Modificado: {row.valor_nuevo or row.valor_anterior or ''}",
		}
		for row in rows
	]


def get_documentos_vet(db: Session, id_usuario: int):
	rows = (
		db.query(
			models.TipoDoc.nombre.label("nombre_documento"),
			models.Documento.id_animal,
			models.Documento.url_archivo,
			models.Estado.nombre.label("estado_documento"),
			models.Documento.fecha_revision,
		)
		.join(models.TipoDoc, models.Documento.id_tipo_doc == models.TipoDoc.id_tipo_doc)
		.join(models.Estado, models.Documento.id_estado == models.Estado.id_estado)
		.filter(models.Documento.id_usuario_subio == id_usuario)
		.order_by(models.TipoDoc.nombre.asc())
		.all()
	)
	return [
		{
			"nombre_documento": row.nombre_documento,
			"id_animal": row.id_animal,
			"enlace_documento": row.url_archivo,
			"estado_documento": row.estado_documento,
			"fecha_revision": row.fecha_revision,
		}
		for row in rows
	]
