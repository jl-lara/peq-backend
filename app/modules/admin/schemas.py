"""Schemas expuestos por el modulo admin."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import (
	BitacoraCreate,
	BitacoraResponse,
	CategoriaGanadoCreate,
	CategoriaGanadoResponse,
	DocumentoCreate,
	DocumentoResponse,
	EnfermedadAnimalCreate,
	EnfermedadAnimalResponse,
	EnfermedadCreate,
	EnfermedadResponse,
	PrecioAnimalCreate,
	PrecioAnimalResponse,
	PrecioCreate,
	PrecioResponse,
	RazaCreate,
	RazaResponse,
	RequisitoDocRolCreate,
	RequisitoDocRolResponse,
	RequisitoDocRolUpdate,
	TipoDocCreate,
	TipoDocResponse,
)


class ResumenUsuariosActivosResponse(BaseModel):
	tipo_usuario: str
	total_usuarios_activos: int


class SolicitudRegistroAdminResponse(BaseModel):
	id_usuario: int
	id_usuario_display: str
	nombre_completo: str
	tipo_rol: str
	email: str
	telefono: Optional[str] = None
	fecha_solicitud: datetime
	estado_usuario: str


class LogActividadAdminResponse(BaseModel):
	fecha_hora: datetime
	usuario_responsable: str
	tipo_usuario: str
	accion: str
	entidad: str
	detalles: str
	ciudad: Optional[str] = None


class DocumentoRevisionAdminResponse(BaseModel):
	id_doc_animal: int
	id_usuario_subio: int
	tipo_documento: str
	enlace_documento: str
	estado_revision: str
	notas_administrador: Optional[str] = None
	fecha_revision: Optional[datetime] = None


class PerfilAdministradorResponse(BaseModel):
	id_usuario: int
	nombre_completo: str
	email: str
	telefono: Optional[str] = None
	ciudad: Optional[str] = None
	rol_sistema: str
	miembro_desde: datetime
	estatus_cuenta: str

__all__ = [
	"BitacoraCreate",
	"BitacoraResponse",
	"CategoriaGanadoCreate",
	"CategoriaGanadoResponse",
	"DocumentoCreate",
	"DocumentoResponse",
	"EnfermedadAnimalCreate",
	"EnfermedadAnimalResponse",
	"EnfermedadCreate",
	"EnfermedadResponse",
	"PrecioAnimalCreate",
	"PrecioAnimalResponse",
	"PrecioCreate",
	"PrecioResponse",
	"RazaCreate",
	"RazaResponse",
	"RequisitoDocRolCreate",
	"RequisitoDocRolResponse",
	"RequisitoDocRolUpdate",
	"ResumenUsuariosActivosResponse",
	"SolicitudRegistroAdminResponse",
	"LogActividadAdminResponse",
	"DocumentoRevisionAdminResponse",
	"PerfilAdministradorResponse",
	"TipoDocCreate",
	"TipoDocResponse",
]
