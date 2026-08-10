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

__all__ = [
	"ResumenGeneralPanel",
	"DesgloseCategoriaPanel",
	"PanelProductorResponse",
	"AnimalRegistradoProductorResponse",
]
