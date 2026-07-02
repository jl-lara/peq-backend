from pydantic import BaseModel
from typing import Optional

# ==========================================
# ESQUEMAS PARA 'ESTADOS'
# ==========================================
class EstadoBase(BaseModel):
    nombre: str

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

class AnimalCreate(AnimalBase):
    pass

class AnimalResponse(AnimalBase):
    id_animal: int
    # No exponemos campos autogenerados de auditoría por ahora

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
from datetime import datetime

class SolicitudCertificacionBase(BaseModel):
    id_estado: int
    id_animal: int
    id_veterinario: Optional[int] = None
    fecha_revision: Optional[datetime] = None
    fecha_dictamen: Optional[datetime] = None

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

class RequisitoDocRolResponse(RequisitoDocRolBase):
    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'DOCUMENTOS'
# ==========================================
from datetime import datetime

class DocumentoBase(BaseModel):
    id_usuario_subio: int
    id_validador: Optional[int] = None
    id_estado: int
    id_tipo_doc: int
    uri_archivo: str
    notas: Optional[str] = None
    fecha_revision: Optional[datetime] = None

class DocumentoCreate(DocumentoBase):
    pass

class DocumentoResponse(DocumentoBase):
    id_documento: int

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
    precio_mercado: float

class PrecioCreate(PrecioBase):
    pass

class PrecioResponse(PrecioBase):
    id_precio: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA 'AUTENTICACIÓN'
# ==========================================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None