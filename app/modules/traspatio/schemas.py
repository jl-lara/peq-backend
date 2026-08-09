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


__all__ = [
	"AnimalResponse",
	"AnimalRegistradoProductorResponse",
	"DocumentoResponse",
	"ProductorResponse",
	"SolicitudCertificacionResponse",
]
