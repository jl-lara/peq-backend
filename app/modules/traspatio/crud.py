"""Consultas del modulo traspatio basadas en el usuario autenticado."""

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import models


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


def get_mis_documentos(
	db: Session,
	id_usuario: int,
	skip: int = 0,
	limit: int = 100,
	id_estado: int | None = None,
	id_tipo_doc: int | None = None,
	fecha_subida_desde: datetime | None = None,
	fecha_subida_hasta: datetime | None = None,
):
	query = db.query(models.Documento).filter(models.Documento.id_usuario_subio == id_usuario)
	if id_estado is not None:
		query = query.filter(models.Documento.id_estado == id_estado)
	if id_tipo_doc is not None:
		query = query.filter(models.Documento.id_tipo_doc == id_tipo_doc)
	if fecha_subida_desde is not None:
		query = query.filter(models.Documento.fecha_subida >= fecha_subida_desde)
	if fecha_subida_hasta is not None:
		query = query.filter(models.Documento.fecha_subida <= fecha_subida_hasta)

	return query.offset(skip).limit(limit).all()


def get_mis_solicitudes(
	db: Session,
	id_usuario: int,
	skip: int = 0,
	limit: int = 100,
	id_estado: int | None = None,
	id_animal: int | None = None,
	id_veterinario: int | None = None,
	fecha_solicitud_desde: datetime | None = None,
	fecha_solicitud_hasta: datetime | None = None,
):
	productor = _get_productor_for_user(db=db, id_usuario=id_usuario)

	query = (
		db.query(models.SolicitudCertificacion)
		.join(models.Animal, models.SolicitudCertificacion.id_animal == models.Animal.id_animal)
		.filter(models.Animal.id_productor == productor.id_productor)
	)
	if id_estado is not None:
		query = query.filter(models.SolicitudCertificacion.id_estado == id_estado)
	if id_animal is not None:
		query = query.filter(models.SolicitudCertificacion.id_animal == id_animal)
	if id_veterinario is not None:
		query = query.filter(models.SolicitudCertificacion.id_veterinario == id_veterinario)
	if fecha_solicitud_desde is not None:
		query = query.filter(models.SolicitudCertificacion.fecha_solicitud >= fecha_solicitud_desde)
	if fecha_solicitud_hasta is not None:
		query = query.filter(models.SolicitudCertificacion.fecha_solicitud <= fecha_solicitud_hasta)

	return query.offset(skip).limit(limit).all()


def get_mis_actividades(
	db: Session,
	id_usuario: int,
	skip: int = 0,
	limit: int = 100,
):
	rows = (
		db.query(
			models.Bitacora.fecha_cambio.label("fecha_hora"),
			models.Accion.nombre.label("accion"),
			models.Bitacora.tabla_afectada.label("entidad"),
			func.concat(
				"ID Afectado: ",
				func.coalesce(models.Bitacora.valor_nuevo, models.Bitacora.valor_anterior),
			).label("detalles"),
		)
		.join(models.Accion, models.Bitacora.id_accion == models.Accion.id_accion)
		.filter(models.Bitacora.id_usuario == id_usuario)
		.order_by(models.Bitacora.fecha_cambio.desc())
		.offset(skip)
		.limit(limit)
		.all()
	)

	return [
		{
			"fecha_hora": row.fecha_hora,
			"accion": row.accion,
			"entidad": row.entidad,
			"detalles": row.detalles,
		}
		for row in rows
	]

def get_perfil_productor(db: Session, id_usuario: int):
	row = (
		db.query(
			(models.Usuario.nombre + " " + models.Usuario.apellido_paterno).label("nombre_completo"),
			models.Usuario.email,
			models.Usuario.telefono,
			models.Rol.nombre.label("tipo_productor"),
			models.Usuario.fecha_registro,
			models.Productor.nombre.label("nombre_rancho"),
			models.Usuario.ciudad.label("municipio"),
			models.Estado.nombre.label("estado_ubicacion"),
			models.Productor.direccion,
			models.Productor.capacidad_animales,
			models.Productor.superficie_hectareas,
		)
		.join(models.Productor, models.Usuario.id_usuario == models.Productor.id_usuario)
		.join(models.Rol, models.Usuario.id_rol == models.Rol.id_rol)
		.join(models.Estado, models.Usuario.id_estado == models.Estado.id_estado)
		.filter(models.Usuario.id_usuario == id_usuario)
		.first()
	)

	if not row:
		raise HTTPException(
			status_code=404,
			detail="Perfil de productor no encontrado para este usuario.",
		)

	return {
		"nombre_completo": row.nombre_completo,
		"email": row.email,
		"telefono": row.telefono,
		"tipo_productor": row.tipo_productor,
		"fecha_registro": row.fecha_registro,
		"nombre_rancho": row.nombre_rancho,
		"municipio": row.municipio,
		"estado_ubicacion": row.estado_ubicacion,
		"direccion": row.direccion,
		"capacidad_animales": row.capacidad_animales,
		"superficie_hectareas": float(row.superficie_hectareas or 0),
	}

def get_documentos_productor(db: Session, id_usuario: int):
	rows = (
		db.query(
			models.TipoDoc.nombre.label("tipo_documento"),
			models.Documento.url_archivo.label("enlace_archivo"),
		)
		.join(models.TipoDoc, models.Documento.id_tipo_doc == models.TipoDoc.id_tipo_doc)
		.filter(models.Documento.id_usuario_subio == id_usuario)
		.order_by(models.TipoDoc.nombre.asc())
		.all()
	)

	return [
		{
			"tipo_documento": row.tipo_documento,
			"enlace_archivo": row.enlace_archivo,
		}
		for row in rows
	]

def get_dashboard_productor(db: Session, id_usuario: int):
	# 1. Obtener el id_productor asociado al usuario autenticado
	productor = _get_productor_for_user(db=db, id_usuario=id_usuario)

	# 2. Ejecutar la función de PostgreSQL
	result = db.execute(
		text("SELECT fn_obtener_panel_productor(:id_productor)"),
		{"id_productor": productor.id_productor},
	).scalar()

	return result or {
		"resumen_general": {"limite_permitido": 0, "total_animales_registrados": 0},
		"desglose_categorias": [],
	}


from fastapi import HTTPException
from sqlalchemy import text


def get_ficha_tecnica_animal(db: Session, arete_id: str):
	# 1. Consulta principal de la Ficha Técnica
	query_ficha = text(
		"""
        SELECT 
            a.id_animal,
            a.arete_id AS no_identificacion,
            r.nombre AS raza,
            cg.nombre AS categoria,
            a.sexo,
            a.edad,
            a.peso_kg,
            a.condicion_general,
            a.proposito_produccion,
            a.tiene_crias,
            a.fecha_registro,
            a.notas AS notas_adicionales,
            COALESCE(pa.precio_final, 0) AS precio_venta,
            
            p.nombre AS nombre_rancho,
            rol.nombre AS tipo_rancho,
            (u_prod.nombre || ' ' || u_prod.apellido_paterno)::VARCHAR AS propietario,
            u_prod.telefono AS contacto_propietario,
            (u_prod.ciudad || ', Baja California')::VARCHAR AS ubicacion_origen,
            
            ('Dr. ' || u_vet.nombre || ' ' || u_vet.apellido_paterno)::VARCHAR AS certificado_por,
            dv.cedula_profesional,
            cert.fecha_certificacion,
            (cert.fecha_certificacion + INTERVAL '6 months')::DATE AS proxima_revision_sugerida
            
        FROM animal a
        JOIN raza r ON a.id_raza = r.id_raza
        JOIN categoria_ganado cg ON r.id_categoria = cg.id_categoria
        LEFT JOIN precio_animal pa ON a.id_animal = pa.id_animal
        JOIN productores p ON a.id_productor = p.id_productor
        JOIN usuarios u_prod ON p.id_usuario = u_prod.id_usuario
        JOIN roles rol ON u_prod.id_rol = rol.id_rol
        LEFT JOIN solicitudes_certificacion sc ON a.id_animal = sc.id_animal AND sc.id_estado = 4
        LEFT JOIN certificaciones cert ON sc.id_solicitud = cert.id_solicitud
        LEFT JOIN usuarios u_vet ON sc.id_veterinario = u_vet.id_usuario
        LEFT JOIN datos_veterinarios dv ON u_vet.id_usuario = dv.id_usuario
        WHERE a.arete_id = :arete_id
        LIMIT 1;
    """
	)

	result = db.execute(query_ficha, {"arete_id": arete_id}).mappings().first()

	if not result:
		raise HTTPException(status_code=404, detail="Ficha técnica no encontrada para el arete especificado.")

	# 2. Consulta de Enfermedades / Estatus Médico
	query_enfermedades = text(
		"""
        SELECT 
            e.nombre AS enfermedad,
            ea.estado AS estatus_medico
        FROM enfermedad_animal ea
        JOIN enfermedad e ON ea.id_enfermedad = e.id_enfermedad
        WHERE ea.id_animal = :id_animal;
    """
	)

	enfermedades = db.execute(query_enfermedades, {"id_animal": result["id_animal"]}).mappings().all()

	ficha_dict = dict(result)
	ficha_dict["precio_venta"] = float(ficha_dict["precio_venta"] or 0)
	ficha_dict["enfermedades"] = [dict(e) for e in enfermedades]

	return ficha_dict