"""Esquemas expuestos por el modulo catalogo_publico."""

from typing import Optional

from pydantic import BaseModel, Field


class EstadisticaCertificacionResponse(BaseModel):
	id_categoria: int
	nombre_categoria: str
	total_animales_certificados: int


class CatalogoAnimalResponse(BaseModel):
	no_identificacion: str
	raza_animal: str
	genero: str
	edad_anios: int
	peso_kg: float
	condicion: Optional[str] = None
	precio_venta: Optional[float] = None
	nombre_rancho: str
	tipo_rancho: str
	certificado_por: Optional[str] = None


class FichaTecnicaHistorialMedicoResponse(BaseModel):
	enfermedad: str
	status_medico: str


class FichaTecnicaDatosBaseResponse(BaseModel):
	no_identificacion: str
	raza: str
	categoria: str
	sexo: str
	edad: int
	peso_kg: float
	condicion_general: Optional[str] = None
	proposito_produccion: Optional[str] = None
	tiene_crias: Optional[bool] = None
	fecha_registro: Optional[str] = None
	notas_adicionales: Optional[str] = None
	precio_venta: Optional[float] = None
	nombre_rancho: str
	tipo_rancho: str
	propietario: Optional[str] = None
	contacto_propietario: Optional[str] = None
	ubicacion_origen: Optional[str] = None
	certificado_por: Optional[str] = None
	cedula_profesional: Optional[str] = None
	fecha_certificacion: Optional[str] = None
	proxima_revision_sugerida: Optional[str] = None


class FichaTecnicaQRResponse(BaseModel):
	datos_base: Optional[FichaTecnicaDatosBaseResponse] = None
	historial_medico: list[FichaTecnicaHistorialMedicoResponse] = Field(default_factory=list)


__all__ = [
	"EstadisticaCertificacionResponse",
	"CatalogoAnimalResponse",
	"FichaTecnicaDatosBaseResponse",
	"FichaTecnicaHistorialMedicoResponse",
	"FichaTecnicaQRResponse",
]
