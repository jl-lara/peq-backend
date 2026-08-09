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
	arete_id: str | None = None
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

class DocumentoProductorResponse(BaseModel):
	tipo_documento: str
	enlace_archivo: str

	class Config:
		from_attributes = True


class ResumenGeneralDashboard(BaseModel):
	limite_permitido: int | None = 0
	total_animales_registrados: int = 0


class DesgloseCategoriaDashboard(BaseModel):
	categoria: str
	total_registrados: int


class DashboardProductorResponse(BaseModel):
	resumen_general: ResumenGeneralDashboard
	desglose_categorias: list[DesgloseCategoriaDashboard]


from datetime import date, datetime
from pydantic import BaseModel


class EnfermedadStatus(BaseModel):
	enfermedad: str
	estatus_medico: str


class FichaTecnicaAnimalResponse(BaseModel):
	# 1. Datos Base del Animal
	no_identificacion: str
	raza: str
	categoria: str
	sexo: str
	edad: int
	peso_kg: float
	condicion_general: str | None = None
	proposito_produccion: str | None = None
	tiene_crias: bool | None = False
	fecha_registro: datetime | None = None
	notas_adicionales: str | None = None
	precio_venta: float | None = 0.0

	# 2. Datos del Productor
	nombre_rancho: str
	tipo_rancho: str
	propietario: str
	contacto_propietario: str | None = None
	ubicacion_origen: str | None = None

	# 3. Certificación Veterinaria
	certificado_por: str | None = None
	cedula_profesional: str | None = None
	fecha_certificacion: datetime | None = None
	proxima_revision_sugerida: date | None = None

	# 4. Historial/Etiquetas Sanitarias
	enfermedades: list[EnfermedadStatus] = []

__all__ = [
	"AnimalResponse",
	"AnimalRegistradoProductorResponse",
	"DocumentoResponse",
	"ProductorResponse",
	"SolicitudCertificacionResponse",
	"ActividadProductorResponse",
	"ProductorPerfilResponse",
	"DocumentoProductorResponse",
	"ResumenGeneralDashboard",
	"DesgloseCategoriaDashboard",
	"DashboardProductorResponse",
	"FichaTecnicaAnimalResponse",
	"EnfermedadStatus",
]