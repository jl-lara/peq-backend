from fastapi import status
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Configuramos el motor de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# ==========================================
# CRUD PARA 'ESTADOS'
# ==========================================
def get_estados(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Estado).offset(skip).limit(limit).all()

def create_estado(db: Session, estado: schemas.EstadoCreate):
    db_estado = models.Estado(nombre=estado.nombre)
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado) # Refresca para obtener el ID autogenerado
    return db_estado

# ==========================================
# CRUD PARA 'ROLES'
# ==========================================
def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rol).offset(skip).limit(limit).all()

def create_rol(db: Session, rol: schemas.RolCreate):
    db_rol = models.Rol(nombre=rol.nombre, descripcion=rol.descripcion)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

# ==========================================
# CRUD PARA 'USUARIOS'
# ==========================================
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # 1. Encriptamos la contraseña
    hashed_password = get_password_hash(usuario.password)
    
    # 2. Preparamos el objeto Usuario
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        usuario=usuario.usuario,
        email=usuario.email,
        telefono=usuario.telefono,
        ciudad=usuario.ciudad,
        id_rol=usuario.id_rol,
        id_estado=usuario.id_estado,
        password=hashed_password
    )
    
    db.add(db_usuario)
    
    # 3. Intentamos guardar, y si falla la base de datos, atrapamos el error
    try:
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError as e:
        db.rollback() # ¡Vital! Limpia la transacción fallida para no trabar la BD
        
        # Opcional: Imprime el error real en tu terminal para que tú lo veas
        print(f"Error de integridad en BD: {e}") 
        
        # Le devuelve al frontend un mensaje claro en lugar de un Error 500
        raise HTTPException(
            status_code=400, 
            detail="Error al registrar: Verifica que el id_rol y el id_estado existan, o que el correo/usuario no estén ya registrados."
        )
    
# ==========================================
# CRUD PARA 'PRODUCTORES'
# ==========================================
def get_productores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Productor).offset(skip).limit(limit).all()

def create_productor(db: Session, productor: schemas.ProductorCreate):
    db_productor = models.Productor(**productor.model_dump())
    db.add(db_productor)
    
    try:
        db.commit()
        db.refresh(db_productor)
        return db_productor
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error al registrar: Verifica que el id_usuario exista y no esté vinculado ya a otro productor."
        )

# ==========================================
# CRUD PARA 'ANIMALES'
# ==========================================
def get_animales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Animal).offset(skip).limit(limit).all()

def create_animal(db: Session, animal: schemas.AnimalCreate):
    db_animal = models.Animal(**animal.model_dump())
    db.add(db_animal)
    
    try:
        db.commit()
        db.refresh(db_animal)
        return db_animal
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error al registrar Animal: Verifica que el arete_id sea único y que el id_productor, id_raza e id_estado existan en los catálogos."
        )
    
# ==========================================
# CRUD PARA 'DATOS VETERINARIOS'
# ==========================================
def get_veterinarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DatosVeterinarios).offset(skip).limit(limit).all()

def create_veterinario(db: Session, veterinario: schemas.DatosVeterinariosCreate):
    db_vet = models.DatosVeterinarios(**veterinario.model_dump())
    db.add(db_vet)
    try:
        db.commit()
        db.refresh(db_vet)
        return db_vet
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error al registrar: Verifica que el id_usuario exista y no sea ya un veterinario."
        )

# ==========================================
# CRUD PARA 'SOLICITUDES' Y 'CERTIFICACIONES'
# ==========================================
def get_solicitudes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SolicitudCertificacion).offset(skip).limit(limit).all()

def create_solicitud(db: Session, solicitud: schemas.SolicitudCertificacionCreate):
    db_solicitud = models.SolicitudCertificacion(**solicitud.model_dump())
    db.add(db_solicitud)
    try:
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error al crear solicitud: Verifica que el animal, estado y veterinario existan."
        )

def get_certificaciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Certificacion).offset(skip).limit(limit).all()

def create_certificacion(db: Session, certificacion: schemas.CertificacionCreate):
    db_certificacion = models.Certificacion(**certificacion.model_dump())
    db.add(db_certificacion)
    try:
        db.commit()
        db.refresh(db_certificacion)
        return db_certificacion
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error: Verifica que la solicitud exista y no tenga ya una certificación asociada."
        )
    
# ==========================================
# CRUD PARA 'GESTIÓN DOCUMENTAL'
# ==========================================
def get_tipos_doc(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TipoDoc).offset(skip).limit(limit).all()

def create_tipo_doc(db: Session, tipo_doc: schemas.TipoDocCreate):
    db_tipo_doc = models.TipoDoc(**tipo_doc.model_dump())
    db.add(db_tipo_doc)
    db.commit()
    db.refresh(db_tipo_doc)
    return db_tipo_doc

def get_requisitos_docs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RequisitoDocRol).offset(skip).limit(limit).all()

def create_requisito_doc(db: Session, requisito: schemas.RequisitoDocRolCreate):
    db_requisito = models.RequisitoDocRol(**requisito.model_dump())
    db.add(db_requisito)
    try:
        db.commit()
        db.refresh(db_requisito)
        return db_requisito
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error: Verifica que el id_rol y el id_tipo_doc existan, o que este requisito no esté ya registrado."
        )

def get_documentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Documento).offset(skip).limit(limit).all()

def create_documento(db: Session, documento: schemas.DocumentoCreate):
    db_documento = models.Documento(**documento.model_dump())
    db.add(db_documento)
    try:
        db.commit()
        db.refresh(db_documento)
        return db_documento
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error al registrar documento: Verifica que el usuario, estado y tipo de documento existan."
        )
    
# ==========================================
# CRUD PARA 'CATÁLOGOS GANADEROS'
# ==========================================
def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CategoriaGanado).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaGanadoCreate):
    db_cat = models.CategoriaGanado(**categoria.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_razas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Raza).offset(skip).limit(limit).all()

def create_raza(db: Session, raza: schemas.RazaCreate):
    db_raza = models.Raza(**raza.model_dump())
    db.add(db_raza)
    try:
        db.commit()
        db.refresh(db_raza)
        return db_raza
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error al registrar raza: Verifica que el id_categoria exista."
        )

def get_precios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Precio).offset(skip).limit(limit).all()

def create_precio(db: Session, precio: schemas.PrecioCreate):
    db_precio = models.Precio(**precio.model_dump())
    db.add(db_precio)
    try:
        db.commit()
        db.refresh(db_precio)
        return db_precio
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error al registrar precio: Verifica que el id_categoria exista."
        )

# Agrega esta función al final de crud.py
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.Usuario).filter(models.Usuario.usuario == username).first()
    if not user:
        return False
    # Verificamos la contraseña encriptada
    if not pwd_context.verify(password, user.password):
        return False
    return user