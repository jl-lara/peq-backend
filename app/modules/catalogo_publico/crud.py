"""Adaptador CRUD del modulo catalogo_publico sobre la capa existente."""

import json

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_estadisticas_certificacion(db: Session):
	row = (
		db.execute(
			text("SELECT fn_obtener_estadisticas_certificacion() AS estadisticas"),
		)
		.mappings()
		.first()
	)
	if row is None:
		return []

	estadisticas = row.get("estadisticas")
	if isinstance(estadisticas, str):
		estadisticas = json.loads(estadisticas)

	if not estadisticas:
		return []

	resultado = []
	for estadistica in estadisticas:
		resultado.append(
			{
				"id_categoria": int(estadistica.get("id_categoria") or 0),
				"nombre_categoria": estadistica.get("nombre_categoria") or "",
				"total_animales_certificados": int(estadistica.get("total_animales_certificados") or 0),
			}
		)

	return resultado


def get_catalogo_animales(db: Session, id_categoria: int, id_estado: int = 4):
	row = (
		db.execute(
			text(
				"""
				SELECT fn_obtener_catalogo_animales(:p_id_categoria, :p_id_estado) AS catalogo
				"""
			),
			{
				"p_id_categoria": id_categoria,
				"p_id_estado": id_estado,
			},
		)
		.mappings()
		.first()
	)
	if row is None:
		return []

	catalogo = row.get("catalogo")
	if isinstance(catalogo, str):
		catalogo = json.loads(catalogo)

	if not catalogo:
		return []

	resultado = []
	for animal in catalogo:
		resultado.append(
			{
				"no_identificacion": animal.get("no_identificacion") or "",
				"raza_animal": animal.get("raza_animal") or "",
				"genero": animal.get("genero") or "",
				"edad_anios": int(animal.get("edad_anios") or 0),
				"peso_kg": float(animal.get("peso_kg") or 0),
				"condicion": animal.get("condicion"),
				"precio_venta": float(animal.get("precio_venta")) if animal.get("precio_venta") is not None else None,
				"nombre_rancho": animal.get("nombre_rancho") or "",
				"tipo_rancho": animal.get("tipo_rancho") or "",
				"certificado_por": animal.get("certificado_por"),
			}
		)

	return resultado


def get_ficha_tecnica_qr(db: Session, arete_id: str):
	row = (
		db.execute(
			text(
				"""
				SELECT fn_obtener_ficha_tecnica_qr(:p_arete_id) AS ficha
				"""
			),
			{"p_arete_id": arete_id},
		)
		.mappings()
		.first()
	)
	if row is None:
		return {"datos_base": None, "historial_medico": []}

	ficha = row.get("ficha")
	if isinstance(ficha, str):
		ficha = json.loads(ficha)

	if not ficha:
		return {"datos_base": None, "historial_medico": []}

	datos_base = ficha.get("datos_base")
	if isinstance(datos_base, str):
		datos_base = json.loads(datos_base)

	historial_medico = ficha.get("historial_medico") or []
	if isinstance(historial_medico, str):
		historial_medico = json.loads(historial_medico)

	resultado_historial = []
	for item in historial_medico:
		resultado_historial.append(
			{
				"enfermedad": item.get("enfermedad") or "",
				"status_medico": item.get("status_medico") or "",
			}
		)

	resultado_base = None
	if isinstance(datos_base, dict):
		resultado_base = {
			"no_identificacion": datos_base.get("no_identificacion") or "",
			"raza": datos_base.get("raza") or "",
			"categoria": datos_base.get("categoria") or "",
			"sexo": datos_base.get("sexo") or "",
			"edad": int(datos_base.get("edad") or 0),
			"peso_kg": float(datos_base.get("peso_kg") or 0),
			"condicion_general": datos_base.get("condicion_general"),
			"proposito_produccion": datos_base.get("proposito_produccion"),
			"tiene_crias": datos_base.get("tiene_crias"),
			"fecha_registro": str(datos_base.get("fecha_registro")) if datos_base.get("fecha_registro") is not None else None,
			"notas_adicionales": datos_base.get("notas_adicionales"),
			"precio_venta": float(datos_base.get("precio_venta")) if datos_base.get("precio_venta") is not None else None,
			"nombre_rancho": datos_base.get("nombre_rancho") or "",
			"tipo_rancho": datos_base.get("tipo_rancho") or "",
			"propietario": datos_base.get("propietario"),
			"contacto_propietario": datos_base.get("contacto_propietario"),
			"ubicacion_origen": datos_base.get("ubicacion_origen"),
			"certificado_por": datos_base.get("certificado_por"),
			"cedula_profesional": datos_base.get("cedula_profesional"),
			"fecha_certificacion": str(datos_base.get("fecha_certificacion")) if datos_base.get("fecha_certificacion") is not None else None,
			"proxima_revision_sugerida": str(datos_base.get("proxima_revision_sugerida")) if datos_base.get("proxima_revision_sugerida") is not None else None,
		}

	return {
		"datos_base": resultado_base,
		"historial_medico": resultado_historial,
	}
