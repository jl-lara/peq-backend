from typing import List, Optional
from pydantic import BaseModel, Field


class ResumenGeneralPanel(BaseModel):
	limite_permitido: Optional[int] = 0
	total_animales_registrados: Optional[int] = 0


class DesgloseCategoriaPanel(BaseModel):
	categoria: str
	total_registrados: int


class PanelProductorResponse(BaseModel):
	resumen_general: ResumenGeneralPanel
	desglose_categorias: List[DesgloseCategoriaPanel]

class DocumentoAnimalRequest(BaseModel):
	id_tipo_doc: int
	url_archivo: str
	notas: Optional[str] = None


class EditarAnimalRequest(BaseModel):
	sexo: str = Field(..., min_length=1)
	edad: float = Field(..., ge=0)
	peso_kg: float = Field(..., ge=0)
	condicion_general: str = Field(..., min_length=1)
	proposito_produccion: str = Field(..., min_length=1)
	documentos: Optional[List[DocumentoAnimalRequest]] = []


class AnimalCatalogoResponse(BaseModel):
	no_identificacion: str
	raza_animal: str
	genero: str
	edad_anios: float
	peso_kg: float
	condicion: Optional[str] = None
	precio_venta: Optional[float] = None
	nombre_rancho: Optional[str] = None
	tipo_rancho: Optional[str] = None
	certificado_por: Optional[str] = None

__all__ = [
	"ResumenGeneralPanel",
	"DesgloseCategoriaPanel",
	"PanelProductorResponse",
	"DocumentoAnimalRequest",
	"EditarAnimalRequest",
	"AnimalCatalogoResponse",
]
