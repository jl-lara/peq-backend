"""Schemas expuestos por el modulo traspatio."""

from datetime import datetime

from pydantic import BaseModel

from app.schemas import (
	AnimalResponse,
	DocumentoResponse,
	ProductorResponse,
	SolicitudCertificacionResponse,
)


class AnimalRegistradoProductorResponse(BaseModel):
	id_animal: int
	tipo_animal: str
	raza: str
	edad_anios: int
	peso_kg: float
	estado_certificacion: str
	precio_estimado: float
	fecha_registro: datetime

class ActividadProductorResponse(BaseModel):
	fecha_hora: datetime
	accion: str
	entidad: str
	detalles: str | None = None

class ProductorPerfilResponse(BaseModel):
	nombre_completo: str
	email: str
	telefono: str | None = None
	tipo_productor: str
	fecha_registro: datetime
	nombre_rancho: str
	municipio: str
	estado_ubicacion: str
	direccion: str
	capacidad_animales: int
	superficie_hectareas: float

	class Config:
		from_attributes = True

__all__ = [
	"AnimalResponse",
	"AnimalRegistradoProductorResponse",
	"DocumentoResponse",
	"ProductorResponse",
	"SolicitudCertificacionResponse",
	"ActividadProductorResponse",
	"ProductorPerfilResponse",
]