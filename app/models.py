from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# ==========================================
# 1. CATÁLOGOS BASE (Sin dependencias)
# ==========================================
class Estado(Base):
    __tablename__ = "estados"
    id_estado: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)

    usuarios: Mapped[List["Usuario"]] = relationship(back_populates="estado")
    animales: Mapped[List["Animal"]] = relationship(back_populates="estado")
    documentos: Mapped[List["Documento"]] = relationship(back_populates="estado")
    solicitudes: Mapped[List["SolicitudCertificacion"]] = relationship(back_populates="estado")

class Rol(Base):
    __tablename__ = "roles"
    id_rol: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))

    usuarios: Mapped[List["Usuario"]] = relationship(back_populates="rol")
    requisitos_docs: Mapped[List["RequisitoDocRol"]] = relationship(back_populates="rol")

class Accion(Base):
    __tablename__ = "accion"
    id_accion: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))

    bitacoras: Mapped[List["Bitacora"]] = relationship(back_populates="accion")

class TipoDoc(Base):
    __tablename__ = "tipo_doc"
    id_tipo_doc: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))

    requisitos_roles: Mapped[List["RequisitoDocRol"]] = relationship(back_populates="tipo_doc")
    documentos: Mapped[List["Documento"]] = relationship(back_populates="tipo_doc")

class CategoriaGanado(Base):
    __tablename__ = "categoria_ganado"
    id_categoria: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    razas: Mapped[List["Raza"]] = relationship(back_populates="categoria")
    precios: Mapped[List["Precio"]] = relationship(back_populates="categoria")

# ==========================================
# 2. CATÁLOGOS DEPENDIENTES
# ==========================================
class Raza(Base):
    __tablename__ = "raza"
    id_raza: Mapped[int] = mapped_column(primary_key=True)
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categoria_ganado.id_categoria"))
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))

    categoria: Mapped["CategoriaGanado"] = relationship(back_populates="razas")
    animales: Mapped[List["Animal"]] = relationship(back_populates="raza")

class Precio(Base):
    __tablename__ = "precio"
    id_precio: Mapped[int] = mapped_column(primary_key=True)
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categoria_ganado.id_categoria"))
    precio_mercado: Mapped[float] = mapped_column(Float, nullable=False)

    categoria: Mapped["CategoriaGanado"] = relationship(back_populates="precios")
    precios_animales: Mapped[List["PrecioAnimal"]] = relationship(back_populates="precio")

# ==========================================
# 3. TABLAS INTERMEDIAS (N:M)
# ==========================================
class RequisitoDocRol(Base):
    __tablename__ = "requisitos_docs_rol"
    id_rol: Mapped[int] = mapped_column(ForeignKey("roles.id_rol"), primary_key=True)
    id_tipo_doc: Mapped[int] = mapped_column(ForeignKey("tipo_doc.id_tipo_doc"), primary_key=True)
    obligatorio: Mapped[bool] = mapped_column(Boolean, default=True)

    rol: Mapped["Rol"] = relationship(back_populates="requisitos_docs")
    tipo_doc: Mapped["TipoDoc"] = relationship(back_populates="requisitos_roles")

class PrecioAnimal(Base):
    __tablename__ = "precio_animal"
    id_precio: Mapped[int] = mapped_column(ForeignKey("precio.id_precio"), primary_key=True)
    id_animal: Mapped[int] = mapped_column(ForeignKey("animal.id_animal"), primary_key=True)
    precio_calidad: Mapped[Optional[float]] = mapped_column(Float)
    precio_final: Mapped[Optional[float]] = mapped_column(Float)

    precio: Mapped["Precio"] = relationship(back_populates="precios_animales")
    animal: Mapped["Animal"] = relationship(back_populates="precios_animales")

# ==========================================
# 4. NÚCLEO DE USUARIOS Y ROLES
# ==========================================
class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido_paterno: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido_materno: Mapped[Optional[str]] = mapped_column(String(100))
    usuario: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    fecha_registro: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    ciudad: Mapped[Optional[str]] = mapped_column(String(100))
    
    id_rol: Mapped[int] = mapped_column(ForeignKey("roles.id_rol"))
    id_estado: Mapped[int] = mapped_column(ForeignKey("estados.id_estado"))

    rol: Mapped["Rol"] = relationship(back_populates="usuarios")
    estado: Mapped["Estado"] = relationship(back_populates="usuarios")
    
    productor: Mapped[Optional["Productor"]] = relationship(back_populates="usuario_vinculado", uselist=False)
    datos_veterinario: Mapped[Optional["DatosVeterinarios"]] = relationship(back_populates="usuario_vinculado", uselist=False)
    
    # Documentos (El usuario puede ser el que sube o el validador)
    documentos_subidos: Mapped[List["Documento"]] = relationship(foreign_keys="[Documento.id_usuario_subio]", back_populates="usuario_subio")
    documentos_validados: Mapped[List["Documento"]] = relationship(foreign_keys="[Documento.id_validador]", back_populates="validador")
    
    solicitudes_veterinario: Mapped[List["SolicitudCertificacion"]] = relationship(back_populates="veterinario")
    bitacoras: Mapped[List["Bitacora"]] = relationship(back_populates="usuario")

class Productor(Base):
    __tablename__ = "productores"
    id_productor: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), unique=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(255))
    capacidad_animales: Mapped[Optional[int]] = mapped_column(Integer)
    superficie_hectareas: Mapped[Optional[float]] = mapped_column(Float)

    usuario_vinculado: Mapped["Usuario"] = relationship(back_populates="productor")
    animales: Mapped[List["Animal"]] = relationship(back_populates="productor")

class DatosVeterinarios(Base):
    __tablename__ = "datos_veterinarios"
    id_docs_vet: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), unique=True)
    cedula_profesional: Mapped[str] = mapped_column(String(50), nullable=False)
    especialidad: Mapped[Optional[str]] = mapped_column(String(100))
    universidad: Mapped[Optional[str]] = mapped_column(String(150))

    usuario_vinculado: Mapped["Usuario"] = relationship(back_populates="datos_veterinario")

# ==========================================
# 5. NEGOCIO Y AUDITORÍA
# ==========================================
class Animal(Base):
    __tablename__ = "animal"
    id_animal: Mapped[int] = mapped_column(primary_key=True)
    arete_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) 
    id_productor: Mapped[int] = mapped_column(ForeignKey("productores.id_productor"))
    id_raza: Mapped[int] = mapped_column(ForeignKey("raza.id_raza")) # ¡Ya activado!
    id_estado: Mapped[int] = mapped_column(ForeignKey("estados.id_estado"))
    
    sexo: Mapped[str] = mapped_column(String(1)) 
    edad: Mapped[int] = mapped_column(Integer) 
    peso_kg: Mapped[float] = mapped_column(Float)
    tiene_crias: Mapped[bool] = mapped_column(Boolean, default=False)
    proposito_produccion: Mapped[str] = mapped_column(String(100)) 
    condicion_general: Mapped[Optional[str]] = mapped_column(String(255))
    fecha_registro: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    fecha_certificacion: Mapped[Optional[datetime]] = mapped_column(DateTime)
    fecha_actualizacion: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    token_qr: Mapped[Optional[str]] = mapped_column(String(255), unique=True)

    productor: Mapped["Productor"] = relationship(back_populates="animales")
    estado: Mapped["Estado"] = relationship(back_populates="animales")
    raza: Mapped["Raza"] = relationship(back_populates="animales")
    precios_animales: Mapped[List["PrecioAnimal"]] = relationship(back_populates="animal")
    solicitudes: Mapped[List["SolicitudCertificacion"]] = relationship(back_populates="animal")

class Documento(Base):
    __tablename__ = "documentos"
    id_documento: Mapped[int] = mapped_column(primary_key=True)
    id_usuario_subio: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    id_validador: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id_usuario"))
    id_estado: Mapped[int] = mapped_column(ForeignKey("estados.id_estado"))
    id_tipo_doc: Mapped[int] = mapped_column(ForeignKey("tipo_doc.id_tipo_doc"))
    uri_archivo: Mapped[str] = mapped_column(String(500), nullable=False)
    notas: Mapped[Optional[str]] = mapped_column(Text)
    fecha_revision: Mapped[Optional[datetime]] = mapped_column(DateTime)

    usuario_subio: Mapped["Usuario"] = relationship(foreign_keys=[id_usuario_subio], back_populates="documentos_subidos")
    validador: Mapped[Optional["Usuario"]] = relationship(foreign_keys=[id_validador], back_populates="documentos_validados")
    estado: Mapped["Estado"] = relationship(back_populates="documentos")
    tipo_doc: Mapped["TipoDoc"] = relationship(back_populates="documentos")

class SolicitudCertificacion(Base):
    __tablename__ = "solicitudes_certificacion"
    id_solicitud: Mapped[int] = mapped_column(primary_key=True)
    id_estado: Mapped[int] = mapped_column(ForeignKey("estados.id_estado"))
    id_animal: Mapped[int] = mapped_column(ForeignKey("animal.id_animal"))
    id_veterinario: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id_usuario"))
    fecha_solicitud: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    fecha_revision: Mapped[Optional[datetime]] = mapped_column(DateTime)
    fecha_dictamen: Mapped[Optional[datetime]] = mapped_column(DateTime)

    estado: Mapped["Estado"] = relationship(back_populates="solicitudes")
    animal: Mapped["Animal"] = relationship(back_populates="solicitudes")
    veterinario: Mapped[Optional["Usuario"]] = relationship(back_populates="solicitudes_veterinario")
    certificacion: Mapped[Optional["Certificacion"]] = relationship(back_populates="solicitud", uselist=False)

class Certificacion(Base):
    __tablename__ = "certificaciones"
    id_certificacion: Mapped[int] = mapped_column(primary_key=True)
    id_solicitud: Mapped[int] = mapped_column(ForeignKey("solicitudes_certificacion.id_solicitud"), unique=True)
    peso_validado: Mapped[float] = mapped_column(Float)
    caracteristicas_validades: Mapped[str] = mapped_column(Text)
    observaciones_medicas: Mapped[Optional[str]] = mapped_column(Text)
    dictamen: Mapped[str] = mapped_column(String(100))
    fecha_certificacion: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    solicitud: Mapped["SolicitudCertificacion"] = relationship(back_populates="certificacion")

class Bitacora(Base):
    __tablename__ = "bitacora"
    id_bitacora: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    id_accion: Mapped[int] = mapped_column(ForeignKey("accion.id_accion"))
    tabla_afectada: Mapped[str] = mapped_column(String(100))
    valor_anterior: Mapped[Optional[str]] = mapped_column(Text)
    valor_nuevo: Mapped[Optional[str]] = mapped_column(Text)
    fecha_cambio: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship(back_populates="bitacoras")
    accion: Mapped["Accion"] = relationship(back_populates="bitacoras")