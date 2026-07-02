from fastapi import FastAPI, Depends, HTTPException, Security, status
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

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "mensaje": "Bienvenido al Backend de PeQ"}

# ==========================================
# ENDPOINTS PARA 'ESTADOS'
# ==========================================
@app.post("/estados/", response_model=schemas.EstadoResponse, tags=["Catálogos - Estados"])
def crear_estado(estado: schemas.EstadoCreate, db: Session = Depends(get_db)):
    return crud.create_estado(db=db, estado=estado)

@app.get("/estados/", response_model=List[schemas.EstadoResponse], tags=["Catálogos - Estados"])
def leer_estados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_estados(db, skip=skip, limit=limit)

# ==========================================
# ENDPOINTS PARA 'ROLES'
# ==========================================
@app.post("/roles/", response_model=schemas.RolResponse, tags=["Catálogos - Roles"])
def crear_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    return crud.create_rol(db=db, rol=rol)

@app.get("/roles/", response_model=List[schemas.RolResponse], tags=["Catálogos - Roles"])
def leer_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_roles(db, skip=skip, limit=limit)

# ==========================================
# ENDPOINTS PARA 'USUARIOS'
# ==========================================
@app.post("/usuarios/", response_model=schemas.UsuarioResponse, tags=["Usuarios"])
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/", response_model=List[schemas.UsuarioResponse], tags=["Usuarios"])
def leer_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_usuarios(db, skip=skip, limit=limit)

# ==========================================
# ENDPOINTS PARA 'PRODUCTORES'
# ==========================================
@app.post("/productores/", response_model=schemas.ProductorResponse, tags=["Productores"])
def crear_productor(productor: schemas.ProductorCreate, db: Session = Depends(get_db)):
    return crud.create_productor(db=db, productor=productor)

@app.get("/productores/", response_model=List[schemas.ProductorResponse], tags=["Productores"])
def leer_productores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_productores(db, skip=skip, limit=limit)

# ==========================================
# ENDPOINTS PARA 'ANIMALES'
# ==========================================
@app.post("/animales/", response_model=schemas.AnimalResponse, tags=["Animales"])
def crear_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    return crud.create_animal(db=db, animal=animal)

@app.get("/animales/", response_model=List[schemas.AnimalResponse], tags=["Animales"])
def leer_animales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_animales(db, skip=skip, limit=limit)

# ==========================================
# ENDPOINTS PARA 'DATOS VETERINARIOS'
# ==========================================
@app.post("/veterinarios/", response_model=schemas.DatosVeterinariosResponse, tags=["Flujo Certificación"])
def crear_veterinario(veterinario: schemas.DatosVeterinariosCreate, db: Session = Depends(get_db)):
    return crud.create_veterinario(db=db, veterinario=veterinario)

@app.get("/veterinarios/", response_model=List[schemas.DatosVeterinariosResponse], tags=["Flujo Certificación"])
def leer_veterinarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_veterinarios(db, skip=skip, limit=limit)

# ==========================================
# ENDPOINTS PARA 'SOLICITUDES Y CERTIFICACIONES'
# ==========================================
@app.post("/solicitudes/", response_model=schemas.SolicitudCertificacionResponse, tags=["Flujo Certificación"])
def crear_solicitud(solicitud: schemas.SolicitudCertificacionCreate, db: Session = Depends(get_db)):
    return crud.create_solicitud(db=db, solicitud=solicitud)

@app.get("/solicitudes/", response_model=List[schemas.SolicitudCertificacionResponse], tags=["Flujo Certificación"])
def leer_solicitudes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_solicitudes(db, skip=skip, limit=limit)

@app.post("/certificaciones/", response_model=schemas.CertificacionResponse, tags=["Flujo Certificación"])
def crear_certificacion(certificacion: schemas.CertificacionCreate, db: Session = Depends(get_db)):
    return crud.create_certificacion(db=db, certificacion=certificacion)

@app.get("/certificaciones/", response_model=List[schemas.CertificacionResponse], tags=["Flujo Certificación"])
def leer_certificaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_certificaciones(db, skip=skip, limit=limit)

# ==========================================
# ENDPOINTS PARA 'GESTIÓN DOCUMENTAL'
# ==========================================
@app.post("/tipos-documentos/", response_model=schemas.TipoDocResponse, tags=["Gestión Documental"])
def crear_tipo_doc(tipo_doc: schemas.TipoDocCreate, db: Session = Depends(get_db)):
    return crud.create_tipo_doc(db=db, tipo_doc=tipo_doc)

@app.get("/tipos-documentos/", response_model=List[schemas.TipoDocResponse], tags=["Gestión Documental"])
def leer_tipos_doc(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tipos_doc(db, skip=skip, limit=limit)

@app.post("/requisitos-documentos/", response_model=schemas.RequisitoDocRolResponse, tags=["Gestión Documental"])
def crear_requisito_doc(requisito: schemas.RequisitoDocRolCreate, db: Session = Depends(get_db)):
    return crud.create_requisito_doc(db=db, requisito=requisito)

@app.get("/requisitos-documentos/", response_model=List[schemas.RequisitoDocRolResponse], tags=["Gestión Documental"])
def leer_requisitos_docs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_requisitos_docs(db, skip=skip, limit=limit)

@app.post("/documentos/", response_model=schemas.DocumentoResponse, tags=["Gestión Documental"])
def crear_documento(documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
    return crud.create_documento(db=db, documento=documento)

@app.get("/documentos/", response_model=List[schemas.DocumentoResponse], tags=["Gestión Documental"])
def leer_documentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_documentos(db, skip=skip, limit=limit)

# ==========================================
# ENDPOINTS PARA 'CATÁLOGOS GANADEROS'
# ==========================================
@app.post("/categorias-ganado/", response_model=schemas.CategoriaGanadoResponse, tags=["Catálogos Ganaderos"])
def crear_categoria(categoria: schemas.CategoriaGanadoCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db=db, categoria=categoria)

@app.get("/categorias-ganado/", response_model=List[schemas.CategoriaGanadoResponse], tags=["Catálogos Ganaderos"])
def leer_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categorias(db, skip=skip, limit=limit)

@app.post("/razas/", response_model=schemas.RazaResponse, tags=["Catálogos Ganaderos"])
def crear_raza(raza: schemas.RazaCreate, db: Session = Depends(get_db)):
    return crud.create_raza(db=db, raza=raza)

@app.get("/razas/", response_model=List[schemas.RazaResponse], tags=["Catálogos Ganaderos"])
def leer_razas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_razas(db, skip=skip, limit=limit)

@app.post("/precios/", response_model=schemas.PrecioResponse, tags=["Catálogos Ganaderos"])
def crear_precio(precio: schemas.PrecioCreate, db: Session = Depends(get_db)):
    return crud.create_precio(db=db, precio=precio)

@app.get("/precios/", response_model=List[schemas.PrecioResponse], tags=["Catálogos Ganaderos"])
def leer_precios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_precios(db, skip=skip, limit=limit)

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