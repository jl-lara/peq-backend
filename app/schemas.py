from datetime import datetime

from pydantic import BaseModel
from pydantic import field_validator, model_validator
from typing import Optional

OFFICIAL_STATES_BY_FLOW: dict[str, set[str]] = {
    "usuario": {"ACTIVO", "INACTIVO", "BLOQUEADO"},
    "animal": {"REGISTRADO", "EN_REVISION", "CERTIFICADO", "RECHAZADO"},
    "solicitud": {"PENDIENTE", "EN_REVISION", "APROBADO", "RECHAZADO"},
    "documento": {"PENDIENTE", "EN_REVISION", "APROBADO", "RECHAZADO"},
}
OFFICIAL_STATE_NAMES: set[str] = set().union(*OFFICIAL_STATES_BY_FLOW.values())

# ==========================================
# ESQUEMAS PARA 'ESTADOS'
# ==========================================
class EstadoBase(BaseModel):
    nombre: str

    @field_validator("nombre")
    @classmethod
    def validar_estado_oficial(cls, value: str) -> str:
        nombre = value.strip().upper()
        if nombre not in OFFICIAL_STATE_NAMES:
            raise ValueError(
                "nombre de estado no oficial. Usa uno del catálogo estándar por flujo."
            )
        return nombre

class EstadoCreate(EstadoBase):
    pass

class EstadoResponse(EstadoBase):
    id_estado: int

    class Config:
        from_attributes = True  # Permite a Pydantic leer los modelos de SQLAlchemy

# ==========================================
# ESQUEMAS PARA 'ROLES'
# ==========================================
class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolResponse(RolBase):
    id_rol: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'ACCIONES'
# ==========================================
class AccionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class AccionCreate(AccionBase):
    pass

class AccionResponse(AccionBase):
    id_accion: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'USUARIOS'
# ==========================================
class UsuarioBase(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    usuario: str
    email: str
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    id_rol: int
    id_estado: int

class UsuarioCreate(UsuarioBase):
    password: str  # Solo lo pedimos al crear

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    fecha_registro: datetime
    # ¡No incluimos el password aquí por seguridad!

    class Config:
        from_attributes = True
    
# ==========================================
# ESQUEMAS PARA 'PRODUCTORES'
# ==========================================
class ProductorBase(BaseModel):
    id_usuario: int
    nombre: str
    direccion: Optional[str] = None
    capacidad_animales: Optional[int] = None
    superficie_hectareas: Optional[float] = None

class ProductorCreate(ProductorBase):
    pass

class ProductorResponse(ProductorBase):
    id_productor: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'ANIMALES'
# ==========================================
class AnimalBase(BaseModel):
    arete_id: str
    id_productor: int
    id_raza: int
    id_estado: int
    sexo: str
    edad: int
    peso_kg: float
    tiene_crias: bool = False
    proposito_produccion: str
    condicion_general: Optional[str] = None
    notas: Optional[str] = None
    color_pelaje: Optional[str] = None
    estado_salud: Optional[str] = None
    foto_frontal: Optional[str] = None
    foto_lateral: Optional[str] = None

    @field_validator("sexo")
    @classmethod
    def validar_sexo(cls, value: str) -> str:
        sexo = value.strip().upper()
        if sexo not in {"M", "F"}:
            raise ValueError("sexo debe ser 'M' o 'F'")
        return sexo

    @field_validator("edad")
    @classmethod
    def validar_edad(cls, value: int) -> int:
        if value < 0 or value > 40:
            raise ValueError("edad debe estar entre 0 y 40")
        return value

    @field_validator("peso_kg")
    @classmethod
    def validar_peso(cls, value: float) -> float:
        if value <= 0 or value > 3000:
            raise ValueError("peso_kg debe ser mayor a 0 y menor o igual a 3000")
        return value

class AnimalCreate(AnimalBase):
    pass

class AnimalResponse(AnimalBase):
    id_animal: int
    fecha_registro: datetime
    fecha_certificacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    token_qr: Optional[str] = None

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'DATOS VETERINARIOS'
# ==========================================
class DatosVeterinariosBase(BaseModel):
    id_usuario: int
    cedula_profesional: str
    especialidad: Optional[str] = None
    universidad: Optional[str] = None

class DatosVeterinariosCreate(DatosVeterinariosBase):
    pass

class DatosVeterinariosResponse(DatosVeterinariosBase):
    id_docs_vet: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'SOLICITUDES DE CERTIFICACIÓN'
# ==========================================

class SolicitudCertificacionBase(BaseModel):
    id_estado: int
    id_animal: int
    id_veterinario: Optional[int] = None
    fecha_revision: Optional[datetime] = None
    fecha_dictamen: Optional[datetime] = None

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_dictamen and not self.fecha_revision:
            raise ValueError("fecha_dictamen requiere fecha_revision")
        if self.fecha_revision and self.fecha_dictamen and self.fecha_dictamen < self.fecha_revision:
            raise ValueError("fecha_dictamen no puede ser anterior a fecha_revision")
        return self

class SolicitudCertificacionCreate(SolicitudCertificacionBase):
    pass

class SolicitudCertificacionResponse(SolicitudCertificacionBase):
    id_solicitud: int
    fecha_solicitud: datetime

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'CERTIFICACIONES'
# ==========================================
class CertificacionBase(BaseModel):
    id_solicitud: int
    peso_validado: float
    caracteristicas_validades: str
    observaciones_medicas: Optional[str] = None
    dictamen: str

    @field_validator("peso_validado")
    @classmethod
    def validar_peso_validado(cls, value: float) -> float:
        if value <= 0 or value > 3000:
            raise ValueError("peso_validado debe ser mayor a 0 y menor o igual a 3000")
        return value

    @field_validator("dictamen")
    @classmethod
    def validar_dictamen(cls, value: str) -> str:
        dictamen = value.strip().upper()
        permitidos = {"APROBADO", "RECHAZADO", "OBSERVADO"}
        if dictamen not in permitidos:
            raise ValueError("dictamen debe ser APROBADO, RECHAZADO u OBSERVADO")
        return dictamen

class CertificacionCreate(CertificacionBase):
    pass

class CertificacionResponse(CertificacionBase):
    id_certificacion: int
    fecha_certificacion: datetime

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'TIPOS DE DOCUMENTOS'
# ==========================================
class TipoDocBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TipoDocCreate(TipoDocBase):
    pass

class TipoDocResponse(TipoDocBase):
    id_tipo_doc: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'REQUISITOS DOCS ROL'
# ==========================================
class RequisitoDocRolBase(BaseModel):
    id_rol: int
    id_tipo_doc: int
    obligatorio: bool = True

class RequisitoDocRolCreate(RequisitoDocRolBase):
    pass

class RequisitoDocRolUpdate(BaseModel):
    obligatorio: bool

class RequisitoDocRolResponse(RequisitoDocRolBase):
    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'DOCUMENTOS'
# ==========================================

class DocumentoBase(BaseModel):
    id_usuario_subio: int
    id_validador: Optional[int] = None
    id_estado: int
    id_tipo_doc: int
    url_archivo: str
    notas: Optional[str] = None
    fecha_subida: Optional[datetime] = None
    fecha_revision: Optional[datetime] = None

class DocumentoCreate(DocumentoBase):
    pass

class DocumentoResponse(DocumentoBase):
    id_doc_animal: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'BITÁCORA'
# ==========================================
class BitacoraBase(BaseModel):
    id_usuario: int
    id_accion: int
    tabla_afectada: str
    valor_anterior: Optional[str] = None
    valor_nuevo: Optional[str] = None
    fecha_cambio: Optional[datetime] = None

class BitacoraCreate(BitacoraBase):
    pass

class BitacoraResponse(BitacoraBase):
    id_bitacora: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'CATÁLOGOS GANADEROS'
# ==========================================
class CategoriaGanadoBase(BaseModel):
    nombre: str

class CategoriaGanadoCreate(CategoriaGanadoBase):
    pass

class CategoriaGanadoResponse(CategoriaGanadoBase):
    id_categoria: int

    class Config:
        from_attributes = True

class RazaBase(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None

class RazaCreate(RazaBase):
    pass

class RazaResponse(RazaBase):
    id_raza: int

    class Config:
        from_attributes = True

class PrecioBase(BaseModel):
    id_categoria: int
    precio_base_kilo: float
    fecha_vigencia: Optional[datetime] = None
    activo: bool = True

class PrecioCreate(PrecioBase):
    pass

class PrecioResponse(PrecioBase):
    id_precio: int

    class Config:
        from_attributes = True

class PrecioAnimalBase(BaseModel):
    id_precio: int
    id_animal: int
    valor_agregado: Optional[float] = None
    modificador_porcentual: Optional[float] = None
    precio_base_aplicado: Optional[float] = None
    peso_al_calculo: Optional[float] = None
    precio_final: Optional[float] = None
    fecha_calculo: Optional[datetime] = None

class PrecioAnimalCreate(PrecioAnimalBase):
    pass

class PrecioAnimalResponse(PrecioAnimalBase):
    class Config:
        from_attributes = True

class EnfermedadBase(BaseModel):
    nombre: str
    porcentaje_penalizacion: float
    requiere_cuarentena: bool = False

    @field_validator("porcentaje_penalizacion")
    @classmethod
    def validar_porcentaje_penalizacion(cls, value: float) -> float:
        if value < 0 or value > 100:
            raise ValueError("porcentaje_penalizacion debe estar entre 0 y 100")
        return value

class EnfermedadCreate(EnfermedadBase):
    pass

class EnfermedadResponse(EnfermedadBase):
    id_enfermedad: int

    class Config:
        from_attributes = True

class EnfermedadAnimalBase(BaseModel):
    id_enfermedad: int
    id_animal: int
    fecha_deteccion: Optional[datetime] = None
    estado: str

    @field_validator("estado")
    @classmethod
    def validar_estado_enfermedad(cls, value: str) -> str:
        estado = value.strip().upper()
        permitidos = {"ACTIVA", "CONTROLADA", "RECUPERADA"}
        if estado not in permitidos:
            raise ValueError("estado debe ser ACTIVA, CONTROLADA o RECUPERADA")
        return estado

class EnfermedadAnimalCreate(EnfermedadAnimalBase):
    pass

class EnfermedadAnimalResponse(EnfermedadAnimalBase):
    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'AUTENTICACIÓN'
# ==========================================
class Token(BaseModel):
    access_token: str
    token_type: str
    id_rol: int

class TokenData(BaseModel):
    username: Optional[str] = None