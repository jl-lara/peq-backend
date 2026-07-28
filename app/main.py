from datetime import datetime
import os

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from . import auth, schemas, crud
from .database import get_db

app = FastAPI(
    title="PeQ API - Gestión Ganadera",
    description="Backend para el sistema de trazabilidad y certificación PeQ.",
    version="1.0.0"
)

raw_cors_origins = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:4173",
)
cors_origins = [origin.strip() for origin in raw_cors_origins.split(",") if origin.strip()]
allow_credentials = "*" not in cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else ["http://localhost:3000"],
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

protected_router = APIRouter(dependencies=[Depends(auth.get_current_user)])

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "mensaje": "Bienvenido al Backend de PeQ"}

# ==========================================
# ENDPOINTS PARA 'ESTADOS'
# ==========================================
@protected_router.post("/estados/", response_model=schemas.EstadoResponse, tags=["Catálogos - Estados"])
def crear_estado(estado: schemas.EstadoCreate, db: Session = Depends(get_db)):
    return crud.create_estado(db=db, estado=estado)

@protected_router.get("/estados/", response_model=List[schemas.EstadoResponse], tags=["Catálogos - Estados"])
def leer_estados(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
    return crud.get_estados(db, skip=skip, limit=limit, nombre=nombre)

@protected_router.put("/estados/{id_estado}", response_model=schemas.EstadoResponse, tags=["Catálogos - Estados"])
def actualizar_estado(id_estado: int, estado: schemas.EstadoCreate, db: Session = Depends(get_db)):
    return crud.update_estado(db=db, id_estado=id_estado, estado=estado)

@protected_router.delete("/estados/{id_estado}", tags=["Catálogos - Estados"])
def eliminar_estado(id_estado: int, db: Session = Depends(get_db)):
    return crud.delete_estado(db=db, id_estado=id_estado)

# ==========================================
# ENDPOINTS PARA 'ROLES'
# ==========================================
@protected_router.post("/roles/", response_model=schemas.RolResponse, tags=["Catálogos - Roles"])
def crear_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    return crud.create_rol(db=db, rol=rol)

@protected_router.get("/roles/", response_model=List[schemas.RolResponse], tags=["Catálogos - Roles"])
def leer_roles(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
    return crud.get_roles(db, skip=skip, limit=limit, nombre=nombre)

@protected_router.put("/roles/{id_rol}", response_model=schemas.RolResponse, tags=["Catálogos - Roles"])
def actualizar_rol(id_rol: int, rol: schemas.RolCreate, db: Session = Depends(get_db)):
    return crud.update_rol(db=db, id_rol=id_rol, rol=rol)

@protected_router.delete("/roles/{id_rol}", tags=["Catálogos - Roles"])
def eliminar_rol(id_rol: int, db: Session = Depends(get_db)):
    return crud.delete_rol(db=db, id_rol=id_rol)

# ==========================================
# ENDPOINTS PARA 'ACCIONES'
# ==========================================
@protected_router.post("/acciones/", response_model=schemas.AccionResponse, tags=["Auditoría"])
def crear_accion(accion: schemas.AccionCreate, db: Session = Depends(get_db)):
    return crud.create_accion(db=db, accion=accion)

@protected_router.get("/acciones/", response_model=List[schemas.AccionResponse], tags=["Auditoría"])
def leer_acciones(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
    return crud.get_acciones(db, skip=skip, limit=limit, nombre=nombre)

@protected_router.put("/acciones/{id_accion}", response_model=schemas.AccionResponse, tags=["Auditoría"])
def actualizar_accion(id_accion: int, accion: schemas.AccionCreate, db: Session = Depends(get_db)):
    return crud.update_accion(db=db, id_accion=id_accion, accion=accion)

@protected_router.delete("/acciones/{id_accion}", tags=["Auditoría"])
def eliminar_accion(id_accion: int, db: Session = Depends(get_db)):
    return crud.delete_accion(db=db, id_accion=id_accion)

# ==========================================
# ENDPOINTS PARA 'USUARIOS'
# ==========================================
@protected_router.post("/usuarios/", response_model=schemas.UsuarioResponse, tags=["Usuarios"])
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

@protected_router.get("/usuarios/", response_model=List[schemas.UsuarioResponse], tags=["Usuarios"])
def leer_usuarios(
    skip: int = 0,
    limit: int = 100,
    id_rol: int | None = None,
    id_estado: int | None = None,
    ciudad: str | None = None,
    usuario: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_usuarios(
        db,
        skip=skip,
        limit=limit,
        id_rol=id_rol,
        id_estado=id_estado,
        ciudad=ciudad,
        usuario=usuario,
        email=email,
    )

@protected_router.put("/usuarios/{id_usuario}", response_model=schemas.UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario(id_usuario: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.update_usuario(db=db, id_usuario=id_usuario, usuario=usuario)

@protected_router.delete("/usuarios/{id_usuario}", tags=["Usuarios"])
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return crud.delete_usuario(db=db, id_usuario=id_usuario)

# ==========================================
# ENDPOINTS PARA 'PRODUCTORES'
# ==========================================
@protected_router.post("/productores/", response_model=schemas.ProductorResponse, tags=["Productores"])
def crear_productor(productor: schemas.ProductorCreate, db: Session = Depends(get_db)):
    return crud.create_productor(db=db, productor=productor)

@protected_router.get("/productores/", response_model=List[schemas.ProductorResponse], tags=["Productores"])
def leer_productores(
    skip: int = 0,
    limit: int = 100,
    id_usuario: int | None = None,
    nombre: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_productores(db, skip=skip, limit=limit, id_usuario=id_usuario, nombre=nombre)

@protected_router.put("/productores/{id_productor}", response_model=schemas.ProductorResponse, tags=["Productores"])
def actualizar_productor(id_productor: int, productor: schemas.ProductorCreate, db: Session = Depends(get_db)):
    return crud.update_productor(db=db, id_productor=id_productor, productor=productor)

@protected_router.delete("/productores/{id_productor}", tags=["Productores"])
def eliminar_productor(id_productor: int, db: Session = Depends(get_db)):
    return crud.delete_productor(db=db, id_productor=id_productor)

# ==========================================
# ENDPOINTS PARA 'ANIMALES'
# ==========================================
@protected_router.post("/animales/", response_model=schemas.AnimalResponse, tags=["Animales"])
def crear_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    return crud.create_animal(db=db, animal=animal)

@protected_router.get("/animales/", response_model=List[schemas.AnimalResponse], tags=["Animales"])
def leer_animales(
    skip: int = 0,
    limit: int = 100,
    id_productor: int | None = None,
    id_raza: int | None = None,
    id_estado: int | None = None,
    sexo: str | None = None,
    edad_min: int | None = None,
    edad_max: int | None = None,
    peso_min: float | None = None,
    peso_max: float | None = None,
    arete_id: str | None = None,
    proposito_produccion: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_animales(
        db,
        skip=skip,
        limit=limit,
        id_productor=id_productor,
        id_raza=id_raza,
        id_estado=id_estado,
        sexo=sexo,
        edad_min=edad_min,
        edad_max=edad_max,
        peso_min=peso_min,
        peso_max=peso_max,
        arete_id=arete_id,
        proposito_produccion=proposito_produccion,
    )

@protected_router.put("/animales/{id_animal}", response_model=schemas.AnimalResponse, tags=["Animales"])
def actualizar_animal(id_animal: int, animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    return crud.update_animal(db=db, id_animal=id_animal, animal=animal)

@protected_router.delete("/animales/{id_animal}", tags=["Animales"])
def eliminar_animal(id_animal: int, db: Session = Depends(get_db)):
    return crud.delete_animal(db=db, id_animal=id_animal)

# ==========================================
# ENDPOINTS PARA 'DATOS VETERINARIOS'
# ==========================================
@protected_router.post("/veterinarios/", response_model=schemas.DatosVeterinariosResponse, tags=["Flujo Certificación"])
def crear_veterinario(veterinario: schemas.DatosVeterinariosCreate, db: Session = Depends(get_db)):
    return crud.create_veterinario(db=db, veterinario=veterinario)

@protected_router.get("/veterinarios/", response_model=List[schemas.DatosVeterinariosResponse], tags=["Flujo Certificación"])
def leer_veterinarios(
    skip: int = 0,
    limit: int = 100,
    id_usuario: int | None = None,
    cedula_profesional: str | None = None,
    especialidad: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_veterinarios(
        db,
        skip=skip,
        limit=limit,
        id_usuario=id_usuario,
        cedula_profesional=cedula_profesional,
        especialidad=especialidad,
    )

@protected_router.put("/veterinarios/{id_docs_vet}", response_model=schemas.DatosVeterinariosResponse, tags=["Flujo Certificación"])
def actualizar_veterinario(id_docs_vet: int, veterinario: schemas.DatosVeterinariosCreate, db: Session = Depends(get_db)):
    return crud.update_veterinario(db=db, id_docs_vet=id_docs_vet, veterinario=veterinario)

@protected_router.delete("/veterinarios/{id_docs_vet}", tags=["Flujo Certificación"])
def eliminar_veterinario(id_docs_vet: int, db: Session = Depends(get_db)):
    return crud.delete_veterinario(db=db, id_docs_vet=id_docs_vet)

# ==========================================
# ENDPOINTS PARA 'SOLICITUDES Y CERTIFICACIONES'
# ==========================================
@protected_router.post("/solicitudes/", response_model=schemas.SolicitudCertificacionResponse, tags=["Flujo Certificación"])
def crear_solicitud(solicitud: schemas.SolicitudCertificacionCreate, db: Session = Depends(get_db)):
    return crud.create_solicitud(db=db, solicitud=solicitud)

@protected_router.get("/solicitudes/", response_model=List[schemas.SolicitudCertificacionResponse], tags=["Flujo Certificación"])
def leer_solicitudes(
    skip: int = 0,
    limit: int = 100,
    id_estado: int | None = None,
    id_animal: int | None = None,
    id_veterinario: int | None = None,
    fecha_solicitud_desde: datetime | None = None,
    fecha_solicitud_hasta: datetime | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_solicitudes(
        db,
        skip=skip,
        limit=limit,
        id_estado=id_estado,
        id_animal=id_animal,
        id_veterinario=id_veterinario,
        fecha_solicitud_desde=fecha_solicitud_desde,
        fecha_solicitud_hasta=fecha_solicitud_hasta,
    )

@protected_router.put("/solicitudes/{id_solicitud}", response_model=schemas.SolicitudCertificacionResponse, tags=["Flujo Certificación"])
def actualizar_solicitud(id_solicitud: int, solicitud: schemas.SolicitudCertificacionCreate, db: Session = Depends(get_db)):
    return crud.update_solicitud(db=db, id_solicitud=id_solicitud, solicitud=solicitud)

@protected_router.delete("/solicitudes/{id_solicitud}", tags=["Flujo Certificación"])
def eliminar_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
    return crud.delete_solicitud(db=db, id_solicitud=id_solicitud)

@protected_router.post("/certificaciones/", response_model=schemas.CertificacionResponse, tags=["Flujo Certificación"])
def crear_certificacion(certificacion: schemas.CertificacionCreate, db: Session = Depends(get_db)):
    return crud.create_certificacion(db=db, certificacion=certificacion)

@protected_router.get("/certificaciones/", response_model=List[schemas.CertificacionResponse], tags=["Flujo Certificación"])
def leer_certificaciones(
    skip: int = 0,
    limit: int = 100,
    id_solicitud: int | None = None,
    dictamen: str | None = None,
    fecha_certificacion_desde: datetime | None = None,
    fecha_certificacion_hasta: datetime | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_certificaciones(
        db,
        skip=skip,
        limit=limit,
        id_solicitud=id_solicitud,
        dictamen=dictamen,
        fecha_certificacion_desde=fecha_certificacion_desde,
        fecha_certificacion_hasta=fecha_certificacion_hasta,
    )

@protected_router.put("/certificaciones/{id_certificacion}", response_model=schemas.CertificacionResponse, tags=["Flujo Certificación"])
def actualizar_certificacion(id_certificacion: int, certificacion: schemas.CertificacionCreate, db: Session = Depends(get_db)):
    return crud.update_certificacion(db=db, id_certificacion=id_certificacion, certificacion=certificacion)

@protected_router.delete("/certificaciones/{id_certificacion}", tags=["Flujo Certificación"])
def eliminar_certificacion(id_certificacion: int, db: Session = Depends(get_db)):
    return crud.delete_certificacion(db=db, id_certificacion=id_certificacion)

# ==========================================
# ENDPOINTS PARA 'GESTIÓN DOCUMENTAL'
# ==========================================
@protected_router.post("/tipos-documentos/", response_model=schemas.TipoDocResponse, tags=["Gestión Documental"])
def crear_tipo_doc(tipo_doc: schemas.TipoDocCreate, db: Session = Depends(get_db)):
    return crud.create_tipo_doc(db=db, tipo_doc=tipo_doc)

@protected_router.get("/tipos-documentos/", response_model=List[schemas.TipoDocResponse], tags=["Gestión Documental"])
def leer_tipos_doc(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
    return crud.get_tipos_doc(db, skip=skip, limit=limit, nombre=nombre)

@protected_router.put("/tipos-documentos/{id_tipo_doc}", response_model=schemas.TipoDocResponse, tags=["Gestión Documental"])
def actualizar_tipo_doc(id_tipo_doc: int, tipo_doc: schemas.TipoDocCreate, db: Session = Depends(get_db)):
    return crud.update_tipo_doc(db=db, id_tipo_doc=id_tipo_doc, tipo_doc=tipo_doc)

@protected_router.delete("/tipos-documentos/{id_tipo_doc}", tags=["Gestión Documental"])
def eliminar_tipo_doc(id_tipo_doc: int, db: Session = Depends(get_db)):
    return crud.delete_tipo_doc(db=db, id_tipo_doc=id_tipo_doc)

@protected_router.post("/requisitos-documentos/", response_model=schemas.RequisitoDocRolResponse, tags=["Gestión Documental"])
def crear_requisito_doc(requisito: schemas.RequisitoDocRolCreate, db: Session = Depends(get_db)):
    return crud.create_requisito_doc(db=db, requisito=requisito)

@protected_router.get("/requisitos-documentos/", response_model=List[schemas.RequisitoDocRolResponse], tags=["Gestión Documental"])
def leer_requisitos_docs(
    skip: int = 0,
    limit: int = 100,
    id_rol: int | None = None,
    id_tipo_doc: int | None = None,
    obligatorio: bool | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_requisitos_docs(
        db,
        skip=skip,
        limit=limit,
        id_rol=id_rol,
        id_tipo_doc=id_tipo_doc,
        obligatorio=obligatorio,
    )

@protected_router.put("/requisitos-documentos/{id_rol}/{id_tipo_doc}", response_model=schemas.RequisitoDocRolResponse, tags=["Gestión Documental"])
def actualizar_requisito_doc(
    id_rol: int,
    id_tipo_doc: int,
    requisito: schemas.RequisitoDocRolUpdate,
    db: Session = Depends(get_db),
):
    return crud.update_requisito_doc(
        db=db,
        id_rol=id_rol,
        id_tipo_doc=id_tipo_doc,
        requisito=requisito,
    )

@protected_router.delete("/requisitos-documentos/{id_rol}/{id_tipo_doc}", tags=["Gestión Documental"])
def eliminar_requisito_doc(id_rol: int, id_tipo_doc: int, db: Session = Depends(get_db)):
    return crud.delete_requisito_doc(db=db, id_rol=id_rol, id_tipo_doc=id_tipo_doc)

@protected_router.post("/documentos/", response_model=schemas.DocumentoResponse, tags=["Gestión Documental"])
def crear_documento(documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
    return crud.create_documento(db=db, documento=documento)

@protected_router.get("/documentos/", response_model=List[schemas.DocumentoResponse], tags=["Gestión Documental"])
def leer_documentos(
    skip: int = 0,
    limit: int = 100,
    id_usuario_subio: int | None = None,
    id_validador: int | None = None,
    id_estado: int | None = None,
    id_tipo_doc: int | None = None,
    fecha_subida_desde: datetime | None = None,
    fecha_subida_hasta: datetime | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_documentos(
        db,
        skip=skip,
        limit=limit,
        id_usuario_subio=id_usuario_subio,
        id_validador=id_validador,
        id_estado=id_estado,
        id_tipo_doc=id_tipo_doc,
        fecha_subida_desde=fecha_subida_desde,
        fecha_subida_hasta=fecha_subida_hasta,
    )

@protected_router.put("/documentos/{id_doc_animal}", response_model=schemas.DocumentoResponse, tags=["Gestión Documental"])
def actualizar_documento(id_doc_animal: int, documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
    return crud.update_documento(db=db, id_doc_animal=id_doc_animal, documento=documento)

@protected_router.delete("/documentos/{id_doc_animal}", tags=["Gestión Documental"])
def eliminar_documento(id_doc_animal: int, db: Session = Depends(get_db)):
    return crud.delete_documento(db=db, id_doc_animal=id_doc_animal)

# ==========================================
# ENDPOINTS PARA 'CATÁLOGOS GANADEROS'
# ==========================================
@protected_router.post("/categorias-ganado/", response_model=schemas.CategoriaGanadoResponse, tags=["Catálogos Ganaderos"])
def crear_categoria(categoria: schemas.CategoriaGanadoCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db=db, categoria=categoria)

@protected_router.get("/categorias-ganado/", response_model=List[schemas.CategoriaGanadoResponse], tags=["Catálogos Ganaderos"])
def leer_categorias(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
    return crud.get_categorias(db, skip=skip, limit=limit, nombre=nombre)

@protected_router.put("/categorias-ganado/{id_categoria}", response_model=schemas.CategoriaGanadoResponse, tags=["Catálogos Ganaderos"])
def actualizar_categoria(id_categoria: int, categoria: schemas.CategoriaGanadoCreate, db: Session = Depends(get_db)):
    return crud.update_categoria(db=db, id_categoria=id_categoria, categoria=categoria)

@protected_router.delete("/categorias-ganado/{id_categoria}", tags=["Catálogos Ganaderos"])
def eliminar_categoria(id_categoria: int, db: Session = Depends(get_db)):
    return crud.delete_categoria(db=db, id_categoria=id_categoria)

@protected_router.post("/razas/", response_model=schemas.RazaResponse, tags=["Catálogos Ganaderos"])
def crear_raza(raza: schemas.RazaCreate, db: Session = Depends(get_db)):
    return crud.create_raza(db=db, raza=raza)

@protected_router.get("/razas/", response_model=List[schemas.RazaResponse], tags=["Catálogos Ganaderos"])
def leer_razas(
    skip: int = 0,
    limit: int = 100,
    id_categoria: int | None = None,
    nombre: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_razas(db, skip=skip, limit=limit, id_categoria=id_categoria, nombre=nombre)

@protected_router.put("/razas/{id_raza}", response_model=schemas.RazaResponse, tags=["Catálogos Ganaderos"])
def actualizar_raza(id_raza: int, raza: schemas.RazaCreate, db: Session = Depends(get_db)):
    return crud.update_raza(db=db, id_raza=id_raza, raza=raza)

@protected_router.delete("/razas/{id_raza}", tags=["Catálogos Ganaderos"])
def eliminar_raza(id_raza: int, db: Session = Depends(get_db)):
    return crud.delete_raza(db=db, id_raza=id_raza)

@protected_router.post("/precios/", response_model=schemas.PrecioResponse, tags=["Catálogos Ganaderos"])
def crear_precio(precio: schemas.PrecioCreate, db: Session = Depends(get_db)):
    return crud.create_precio(db=db, precio=precio)

@protected_router.get("/precios/", response_model=List[schemas.PrecioResponse], tags=["Catálogos Ganaderos"])
def leer_precios(
    skip: int = 0,
    limit: int = 100,
    id_categoria: int | None = None,
    activo: bool | None = None,
    fecha_vigencia_desde: datetime | None = None,
    fecha_vigencia_hasta: datetime | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_precios(
        db,
        skip=skip,
        limit=limit,
        id_categoria=id_categoria,
        activo=activo,
        fecha_vigencia_desde=fecha_vigencia_desde,
        fecha_vigencia_hasta=fecha_vigencia_hasta,
    )

@protected_router.post("/precios-animales/", response_model=schemas.PrecioAnimalResponse, tags=["Catálogos Ganaderos"])
def crear_precio_animal(precio_animal: schemas.PrecioAnimalCreate, db: Session = Depends(get_db)):
    return crud.create_precio_animal(db=db, precio_animal=precio_animal)

@protected_router.get("/precios-animales/", response_model=List[schemas.PrecioAnimalResponse], tags=["Catálogos Ganaderos"])
def leer_precios_animales(
    skip: int = 0,
    limit: int = 100,
    id_precio: int | None = None,
    id_animal: int | None = None,
    fecha_calculo_desde: datetime | None = None,
    fecha_calculo_hasta: datetime | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_precios_animales(
        db,
        skip=skip,
        limit=limit,
        id_precio=id_precio,
        id_animal=id_animal,
        fecha_calculo_desde=fecha_calculo_desde,
        fecha_calculo_hasta=fecha_calculo_hasta,
    )

@protected_router.put("/precios-animales/{id_precio}/{id_animal}", response_model=schemas.PrecioAnimalResponse, tags=["Catálogos Ganaderos"])
def actualizar_precio_animal(
    id_precio: int,
    id_animal: int,
    precio_animal: schemas.PrecioAnimalCreate,
    db: Session = Depends(get_db),
):
    return crud.update_precio_animal(
        db=db,
        id_precio=id_precio,
        id_animal=id_animal,
        precio_animal=precio_animal,
    )

@protected_router.delete("/precios-animales/{id_precio}/{id_animal}", tags=["Catálogos Ganaderos"])
def eliminar_precio_animal(id_precio: int, id_animal: int, db: Session = Depends(get_db)):
    return crud.delete_precio_animal(db=db, id_precio=id_precio, id_animal=id_animal)

# ==========================================
# ENDPOINTS PARA 'BITÁCORA'
# ==========================================
@protected_router.post("/bitacoras/", response_model=schemas.BitacoraResponse, tags=["Auditoría"])
def crear_bitacora(bitacora: schemas.BitacoraCreate, db: Session = Depends(get_db)):
    return crud.create_bitacora(db=db, bitacora=bitacora)

@protected_router.get("/bitacoras/", response_model=List[schemas.BitacoraResponse], tags=["Auditoría"])
def leer_bitacoras(
    skip: int = 0,
    limit: int = 100,
    id_usuario: int | None = None,
    id_accion: int | None = None,
    tabla_afectada: str | None = None,
    fecha_cambio_desde: datetime | None = None,
    fecha_cambio_hasta: datetime | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_bitacoras(
        db,
        skip=skip,
        limit=limit,
        id_usuario=id_usuario,
        id_accion=id_accion,
        tabla_afectada=tabla_afectada,
        fecha_cambio_desde=fecha_cambio_desde,
        fecha_cambio_hasta=fecha_cambio_hasta,
    )

@protected_router.put("/bitacoras/{id_bitacora}", response_model=schemas.BitacoraResponse, tags=["Auditoría"])
def actualizar_bitacora(id_bitacora: int, bitacora: schemas.BitacoraCreate, db: Session = Depends(get_db)):
    return crud.update_bitacora(db=db, id_bitacora=id_bitacora, bitacora=bitacora)

@protected_router.delete("/bitacoras/{id_bitacora}", tags=["Auditoría"])
def eliminar_bitacora(id_bitacora: int, db: Session = Depends(get_db)):
    return crud.delete_bitacora(db=db, id_bitacora=id_bitacora)

# ==========================================
# ENDPOINTS PARA 'SANIDAD ANIMAL'
# ==========================================
@protected_router.post("/enfermedades/", response_model=schemas.EnfermedadResponse, tags=["Sanidad Animal"])
def crear_enfermedad(enfermedad: schemas.EnfermedadCreate, db: Session = Depends(get_db)):
    return crud.create_enfermedad(db=db, enfermedad=enfermedad)

@protected_router.get("/enfermedades/", response_model=List[schemas.EnfermedadResponse], tags=["Sanidad Animal"])
def leer_enfermedades(
    skip: int = 0,
    limit: int = 100,
    nombre: str | None = None,
    requiere_cuarentena: bool | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_enfermedades(
        db,
        skip=skip,
        limit=limit,
        nombre=nombre,
        requiere_cuarentena=requiere_cuarentena,
    )

@protected_router.put("/enfermedades/{id_enfermedad}", response_model=schemas.EnfermedadResponse, tags=["Sanidad Animal"])
def actualizar_enfermedad(id_enfermedad: int, enfermedad: schemas.EnfermedadCreate, db: Session = Depends(get_db)):
    return crud.update_enfermedad(db=db, id_enfermedad=id_enfermedad, enfermedad=enfermedad)

@protected_router.delete("/enfermedades/{id_enfermedad}", tags=["Sanidad Animal"])
def eliminar_enfermedad(id_enfermedad: int, db: Session = Depends(get_db)):
    return crud.delete_enfermedad(db=db, id_enfermedad=id_enfermedad)

@protected_router.post("/enfermedades-animales/", response_model=schemas.EnfermedadAnimalResponse, tags=["Sanidad Animal"])
def crear_enfermedad_animal(enfermedad_animal: schemas.EnfermedadAnimalCreate, db: Session = Depends(get_db)):
    return crud.create_enfermedad_animal(db=db, enfermedad_animal=enfermedad_animal)

@protected_router.get("/enfermedades-animales/", response_model=List[schemas.EnfermedadAnimalResponse], tags=["Sanidad Animal"])
def leer_enfermedades_animales(
    skip: int = 0,
    limit: int = 100,
    id_enfermedad: int | None = None,
    id_animal: int | None = None,
    estado: str | None = None,
    fecha_deteccion_desde: datetime | None = None,
    fecha_deteccion_hasta: datetime | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_enfermedades_animales(
        db,
        skip=skip,
        limit=limit,
        id_enfermedad=id_enfermedad,
        id_animal=id_animal,
        estado=estado,
        fecha_deteccion_desde=fecha_deteccion_desde,
        fecha_deteccion_hasta=fecha_deteccion_hasta,
    )

@protected_router.put("/enfermedades-animales/{id_enfermedad}/{id_animal}", response_model=schemas.EnfermedadAnimalResponse, tags=["Sanidad Animal"])
def actualizar_enfermedad_animal(
    id_enfermedad: int,
    id_animal: int,
    enfermedad_animal: schemas.EnfermedadAnimalCreate,
    db: Session = Depends(get_db),
):
    return crud.update_enfermedad_animal(
        db=db,
        id_enfermedad=id_enfermedad,
        id_animal=id_animal,
        enfermedad_animal=enfermedad_animal,
    )

@protected_router.delete("/enfermedades-animales/{id_enfermedad}/{id_animal}", tags=["Sanidad Animal"])
def eliminar_enfermedad_animal(id_enfermedad: int, id_animal: int, db: Session = Depends(get_db)):
    return crud.delete_enfermedad_animal(db=db, id_enfermedad=id_enfermedad, id_animal=id_animal)

@protected_router.put("/precios/{id_precio}", response_model=schemas.PrecioResponse, tags=["Catálogos Ganaderos"])
def actualizar_precio(id_precio: int, precio: schemas.PrecioCreate, db: Session = Depends(get_db)):
    return crud.update_precio(db=db, id_precio=id_precio, precio=precio)

@protected_router.delete("/precios/{id_precio}", tags=["Catálogos Ganaderos"])
def eliminar_precio(id_precio: int, db: Session = Depends(get_db)):
    return crud.delete_precio(db=db, id_precio=id_precio)

app.include_router(protected_router)

@app.post("/login", response_model=schemas.Token, tags=["Autenticación"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.usuario})
    return {"access_token": access_token, "token_type": "bearer"}