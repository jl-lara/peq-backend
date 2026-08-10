"""Schemas expuestos por el modulo veterinario."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import (
	CertificacionCreate,
	CertificacionResponse,
	DatosVeterinariosCreate,
	DatosVeterinariosResponse,
	SolicitudCertificacionCreate,
	SolicitudCertificacionResponse,
)


class PerfilVeterinarioResponse(BaseModel):
	nombre_completo: str
	email: str
	telefono: Optional[str] = None
	ciudad: Optional[str] = None
	estado_usuario: str
	fecha_registro: datetime
	cedula_profesional: str
	especialidad: Optional[str] = None
	universidad: Optional[str] = None
	total_certificaciones: int


class PerfilVeterinarioResumenResponse(BaseModel):
	certificaciones_realizadas: int
	miembro_desde: datetime


class PerfilVeterinarioDatosPersonalesResponse(BaseModel):
	nombre_completo: str
	curp: Optional[str] = None
	email: str
	telefono: Optional[str] = None
	municipio: Optional[str] = None
	estado: Optional[str] = None


class PerfilVeterinarioDatosProfesionalesResponse(BaseModel):
	cedula_profesional: str
	especialidad: Optional[str] = None
	universidad: Optional[str] = None
	fecha_registro: datetime


class PerfilVeterinarioDetalladoResponse(BaseModel):
	resumen: PerfilVeterinarioResumenResponse
	datos_personales: PerfilVeterinarioDatosPersonalesResponse
	datos_profesionales: PerfilVeterinarioDatosProfesionalesResponse


class PerfilVeterinarioActualizarDBRequest(BaseModel):
	nombre: str
	apellido_paterno: str
	apellido_materno: Optional[str] = None
	email: str
	telefono: Optional[str] = None
	ciudad: Optional[str] = None
	especialidad: Optional[str] = None


class PerfilVeterinarioActualizarDBResponse(BaseModel):
	status: str
	mensaje: str
	id_usuario: int


class RevisionCertificacionVeterinariaDBRequest(BaseModel):
	id_solicitud: int
	peso_validado: float
	caracteristicas_validadas: str
	observaciones_medicas: Optional[str] = None
	dictamen: str
	id_estado_nuevo: int


class RevisionCertificacionVeterinariaDBResponse(BaseModel):
	status: str
	mensaje: str
	id_certificacion: int
	id_solicitud: int


class SolicitudPanelVeterinarioResponse(BaseModel):
	codigo_solicitud: str
	id_solicitud: int
	arete_animal: str
	tipo_ganado: str
	nombre_productor: str
	rancho: str
	raza: str
	edad_anios: int
	peso_est_kg: float
	fecha_solicitud: datetime
	estado_solicitud: str


class SolicitudPanelVeterinarioDBResponse(BaseModel):
	codigo_solicitud: str
	arete_animal: str
	tipo_ganado: str
	nombre_productor: str
	rancho: str
	raza: str
	edad_anios: int
	peso_est_kg: float
	fecha_solicitud: datetime
	estado_solicitud: str


class BitacoraVeterinarioResponse(BaseModel):
	fecha_hora: datetime
	tipo_accion: str
	entidad_afectada: str
	detalles: str


class BitacoraVeterinarioDBResponse(BaseModel):
	fecha_hora: datetime
	tipo_accion: str
	entidad_afectada: str
	detalles: str


class DocumentoVeterinarioResponse(BaseModel):
	nombre_documento: str
	id_animal: Optional[int] = None
	enlace_documento: str
	estado_documento: str
	fecha_revision: Optional[datetime] = None


class DocumentoVeterinarioDBResponse(BaseModel):
	nombre_documento: str
	enlace_documento: str
	estado_documento: str

__all__ = [
	"CertificacionCreate",
	"CertificacionResponse",
	"DatosVeterinariosCreate",
	"DatosVeterinariosResponse",
	"PerfilVeterinarioResponse",
	"SolicitudPanelVeterinarioResponse",
	"BitacoraVeterinarioResponse",
	"BitacoraVeterinarioDBResponse",
	"PerfilVeterinarioDatosPersonalesResponse",
	"PerfilVeterinarioDatosProfesionalesResponse",
	"PerfilVeterinarioDetalladoResponse",
	"PerfilVeterinarioActualizarDBRequest",
	"PerfilVeterinarioActualizarDBResponse",
	"RevisionCertificacionVeterinariaDBRequest",
	"RevisionCertificacionVeterinariaDBResponse",
	"PerfilVeterinarioResumenResponse",
	"DocumentoVeterinarioResponse",
	"DocumentoVeterinarioDBResponse",
	"SolicitudPanelVeterinarioDBResponse",
	"SolicitudCertificacionCreate",
	"SolicitudCertificacionResponse",
]
