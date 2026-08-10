"""Schemas expuestos por el modulo admin."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import (
	BitacoraCreate,
	BitacoraResponse,
	CategoriaGanadoCreate,
	CategoriaGanadoResponse,
	AccionCreate,
	AccionResponse,
	DocumentoCreate,
	DocumentoResponse,
	EnfermedadAnimalCreate,
	EnfermedadAnimalResponse,
	EnfermedadCreate,
	EnfermedadResponse,
	EstadoCreate,
	EstadoResponse,
	PrecioAnimalCreate,
	PrecioAnimalResponse,
	PrecioCreate,
	PrecioResponse,
	RolCreate,
	RolResponse,
	RazaCreate,
	RazaResponse,
	RequisitoDocRolCreate,
	RequisitoDocRolResponse,
	RequisitoDocRolUpdate,
	SolicitudCambioCreate,
	SolicitudCambioResponse,
	UsuarioCreate,
	UsuarioResponse,
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
	id_animal: Optional[int] = None
	id_usuario_subio: int
	tipo_documento: str
	enlace_documento: str
	estado_revision: str
	notas_administrador: Optional[str] = None
	fecha_revision: Optional[datetime] = None


class SolicitudCambioAdminResponse(BaseModel):
	id_solicitud_cambio: int
	id_usuario_solicita: int
	id_usuario_objetivo: Optional[int] = None
	campo_afectado: str
	valor_anterior: Optional[str] = None
	valor_nuevo: Optional[str] = None
	motivo: Optional[str] = None
	id_estado: int
	fecha_solicitud: datetime
	fecha_revision: Optional[datetime] = None
	id_revisor: Optional[int] = None


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
	"AccionCreate",
	"AccionResponse",
	"DocumentoCreate",
	"DocumentoResponse",
	"EnfermedadAnimalCreate",
	"EnfermedadAnimalResponse",
	"EnfermedadCreate",
	"EnfermedadResponse",
	"EstadoCreate",
	"EstadoResponse",
	"PrecioAnimalCreate",
	"PrecioAnimalResponse",
	"PrecioCreate",
	"PrecioResponse",
	"RolCreate",
	"RolResponse",
	"RazaCreate",
	"RazaResponse",
	"RequisitoDocRolCreate",
	"RequisitoDocRolResponse",
	"RequisitoDocRolUpdate",
	"SolicitudCambioCreate",
	"SolicitudCambioResponse",
	"UsuarioCreate",
	"UsuarioResponse",
	"ResumenUsuariosActivosResponse",
	"SolicitudRegistroAdminResponse",
	"LogActividadAdminResponse",
	"DocumentoRevisionAdminResponse",
	"SolicitudCambioAdminResponse",
	"PerfilAdministradorResponse",
	"TipoDocCreate",
	"TipoDocResponse",
]
