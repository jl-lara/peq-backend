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


class BitacoraVeterinarioResponse(BaseModel):
	fecha_hora: datetime
	tipo_accion: str
	entidad_afectada: str
	detalles: str


class DocumentoVeterinarioResponse(BaseModel):
	nombre_documento: str
	enlace_documento: str
	estado_documento: str
	fecha_revision: Optional[datetime] = None

__all__ = [
	"CertificacionCreate",
	"CertificacionResponse",
	"DatosVeterinariosCreate",
	"DatosVeterinariosResponse",
	"PerfilVeterinarioResponse",
	"SolicitudPanelVeterinarioResponse",
	"BitacoraVeterinarioResponse",
	"DocumentoVeterinarioResponse",
	"SolicitudCertificacionCreate",
	"SolicitudCertificacionResponse",
]
