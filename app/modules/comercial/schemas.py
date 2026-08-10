from typing import List, Optional
from pydantic import BaseModel


class ResumenGeneralPanel(BaseModel):
	limite_permitido: Optional[int] = 0
	total_animales_registrados: Optional[int] = 0


class DesgloseCategoriaPanel(BaseModel):
	categoria: str
	total_registrados: int


class PanelProductorResponse(BaseModel):
	resumen_general: ResumenGeneralPanel
	desglose_categorias: List[DesgloseCategoriaPanel]

__all__ = [
	"ResumenGeneralPanel",
	"DesgloseCategoriaPanel",
	"PanelProductorResponse",
]
