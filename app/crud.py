from datetime import datetime
from typing import Optional

from fastapi import status
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt

def get_password_hash(password: str):
    # Genera la sal y hashea la contraseña directamente con bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def _get_estado_or_400(db: Session, id_estado: int) -> models.Estado:
    estado = db.query(models.Estado).filter(models.Estado.id_estado == id_estado).first()
    if not estado:
        raise HTTPException(status_code=400, detail=f"El id_estado {id_estado} no existe.")
    return estado


def _validate_estado_for_flow(db: Session, id_estado: int, flow: str) -> models.Estado:
    estado = _get_estado_or_400(db, id_estado)
    allowed_states = schemas.OFFICIAL_STATES_BY_FLOW[flow]
    estado_name = estado.nombre.strip().upper()
    if estado_name not in allowed_states:
        allowed_values = ", ".join(sorted(allowed_states))
        raise HTTPException(
            status_code=400,
            detail=(
                f"El estado '{estado.nombre}' (id={id_estado}) no es válido para flujo '{flow}'. "
                f"Valores permitidos: {allowed_values}."
            ),
        )
    return estado

# ==========================================
# CRUD PARA 'ESTADOS'
# ==========================================
def get_estados(db: Session, skip: int = 0, limit: int = 100, nombre: Optional[str] = None):
    query = db.query(models.Estado)
    if nombre:
        query = query.filter(models.Estado.nombre == nombre.strip().upper())
    return query.offset(skip).limit(limit).all()

def create_estado(db: Session, estado: schemas.EstadoCreate):
    existing_state = db.query(models.Estado).filter(models.Estado.nombre == estado.nombre).first()
    if existing_state:
        raise HTTPException(
            status_code=400,
            detail=f"El estado '{estado.nombre}' ya existe en el catálogo oficial.",
        )

    db_estado = models.Estado(nombre=estado.nombre)
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado) # Refresca para obtener el ID autogenerado
    return db_estado

# ==========================================
# CRUD PARA 'ROLES'
# ==========================================
def get_roles(db: Session, skip: int = 0, limit: int = 100, nombre: Optional[str] = None):
    query = db.query(models.Rol)
    if nombre:
        query = query.filter(models.Rol.nombre == nombre.strip().upper())
    return query.offset(skip).limit(limit).all()

def create_rol(db: Session, rol: schemas.RolCreate):
    db_rol = models.Rol(nombre=rol.nombre, descripcion=rol.descripcion)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

# ==========================================
# CRUD PARA 'USUARIOS'
# ==========================================
def get_usuarios(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_rol: Optional[int] = None,
    id_estado: Optional[int] = None,
    ciudad: Optional[str] = None,
    usuario: Optional[str] = None,
    email: Optional[str] = None,
):
    query = db.query(models.Usuario)
    if id_rol is not None:
        query = query.filter(models.Usuario.id_rol == id_rol)
    if id_estado is not None:
        query = query.filter(models.Usuario.id_estado == id_estado)
    if ciudad:
        query = query.filter(models.Usuario.ciudad == ciudad)
    if usuario:
        query = query.filter(models.Usuario.usuario == usuario)
    if email:
        query = query.filter(models.Usuario.email == email)
    return query.offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    _validate_estado_for_flow(db, usuario.id_estado, "usuario")

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
def get_productores(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_usuario: Optional[int] = None,
    nombre: Optional[str] = None,
):
    query = db.query(models.Productor)
    if id_usuario is not None:
        query = query.filter(models.Productor.id_usuario == id_usuario)
    if nombre:
        query = query.filter(models.Productor.nombre == nombre)
    return query.offset(skip).limit(limit).all()

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
def get_animales(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_productor: Optional[int] = None,
    id_raza: Optional[int] = None,
    id_estado: Optional[int] = None,
    sexo: Optional[str] = None,
    edad_min: Optional[int] = None,
    edad_max: Optional[int] = None,
    peso_min: Optional[float] = None,
    peso_max: Optional[float] = None,
    arete_id: Optional[str] = None,
    proposito_produccion: Optional[str] = None,
):
    query = db.query(models.Animal)
    if id_productor is not None:
        query = query.filter(models.Animal.id_productor == id_productor)
    if id_raza is not None:
        query = query.filter(models.Animal.id_raza == id_raza)
    if id_estado is not None:
        query = query.filter(models.Animal.id_estado == id_estado)
    if sexo:
        query = query.filter(models.Animal.sexo == sexo.strip().upper())
    if edad_min is not None:
        query = query.filter(models.Animal.edad >= edad_min)
    if edad_max is not None:
        query = query.filter(models.Animal.edad <= edad_max)
    if peso_min is not None:
        query = query.filter(models.Animal.peso_kg >= peso_min)
    if peso_max is not None:
        query = query.filter(models.Animal.peso_kg <= peso_max)
    if arete_id:
        query = query.filter(models.Animal.arete_id == arete_id)
    if proposito_produccion:
        query = query.filter(models.Animal.proposito_produccion == proposito_produccion)
    return query.offset(skip).limit(limit).all()

def create_animal(db: Session, animal: schemas.AnimalCreate):
    _validate_estado_for_flow(db, animal.id_estado, "animal")

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
def get_veterinarios(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_usuario: Optional[int] = None,
    cedula_profesional: Optional[str] = None,
    especialidad: Optional[str] = None,
):
    query = db.query(models.DatosVeterinarios)
    if id_usuario is not None:
        query = query.filter(models.DatosVeterinarios.id_usuario == id_usuario)
    if cedula_profesional:
        query = query.filter(models.DatosVeterinarios.cedula_profesional == cedula_profesional)
    if especialidad:
        query = query.filter(models.DatosVeterinarios.especialidad == especialidad)
    return query.offset(skip).limit(limit).all()

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
def get_solicitudes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_estado: Optional[int] = None,
    id_animal: Optional[int] = None,
    id_veterinario: Optional[int] = None,
    fecha_solicitud_desde: Optional[datetime] = None,
    fecha_solicitud_hasta: Optional[datetime] = None,
):
    query = db.query(models.SolicitudCertificacion)
    if id_estado is not None:
        query = query.filter(models.SolicitudCertificacion.id_estado == id_estado)
    if id_animal is not None:
        query = query.filter(models.SolicitudCertificacion.id_animal == id_animal)
    if id_veterinario is not None:
        query = query.filter(models.SolicitudCertificacion.id_veterinario == id_veterinario)
    if fecha_solicitud_desde is not None:
        query = query.filter(models.SolicitudCertificacion.fecha_solicitud >= fecha_solicitud_desde)
    if fecha_solicitud_hasta is not None:
        query = query.filter(models.SolicitudCertificacion.fecha_solicitud <= fecha_solicitud_hasta)
    return query.offset(skip).limit(limit).all()

def create_solicitud(db: Session, solicitud: schemas.SolicitudCertificacionCreate):
    _validate_estado_for_flow(db, solicitud.id_estado, "solicitud")

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


# ==========================================
# CRUD PARA 'SOLICITUDES DE CAMBIO'
# ==========================================
def get_solicitudes_cambio(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_usuario_solicita: Optional[int] = None,
    id_usuario_objetivo: Optional[int] = None,
    id_revisor: Optional[int] = None,
    id_estado: Optional[int] = None,
    campo_afectado: Optional[str] = None,
    fecha_solicitud_desde: Optional[datetime] = None,
    fecha_solicitud_hasta: Optional[datetime] = None,
):
    query = db.query(models.SolicitudCambio)
    if id_usuario_solicita is not None:
        query = query.filter(models.SolicitudCambio.id_usuario_solicita == id_usuario_solicita)
    if id_usuario_objetivo is not None:
        query = query.filter(models.SolicitudCambio.id_usuario_objetivo == id_usuario_objetivo)
    if id_revisor is not None:
        query = query.filter(models.SolicitudCambio.id_revisor == id_revisor)
    if id_estado is not None:
        query = query.filter(models.SolicitudCambio.id_estado == id_estado)
    if campo_afectado is not None:
        query = query.filter(models.SolicitudCambio.campo_afectado == campo_afectado.strip())
    if fecha_solicitud_desde is not None:
        query = query.filter(models.SolicitudCambio.fecha_solicitud >= fecha_solicitud_desde)
    if fecha_solicitud_hasta is not None:
        query = query.filter(models.SolicitudCambio.fecha_solicitud <= fecha_solicitud_hasta)
    return query.offset(skip).limit(limit).all()


def create_solicitud_cambio(db: Session, solicitud_cambio: schemas.SolicitudCambioCreate):
    _validate_estado_for_flow(db, solicitud_cambio.id_estado, "solicitud")
    _get_entity_or_404(db, models.Usuario, "id_usuario", solicitud_cambio.id_usuario_solicita, "Usuario")
    if solicitud_cambio.id_usuario_objetivo is not None:
        _get_entity_or_404(db, models.Usuario, "id_usuario", solicitud_cambio.id_usuario_objetivo, "Usuario")
    if solicitud_cambio.id_revisor is not None:
        _get_entity_or_404(db, models.Usuario, "id_usuario", solicitud_cambio.id_revisor, "Usuario")

    db_solicitud = models.SolicitudCambio(**solicitud_cambio.model_dump())
    db.add(db_solicitud)
    try:
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al crear solicitud de cambio: Verifica usuarios, estado y consistencia de datos.",
        )


def update_solicitud_cambio(db: Session, id_solicitud_cambio: int, solicitud_cambio: schemas.SolicitudCambioCreate):
    _validate_estado_for_flow(db, solicitud_cambio.id_estado, "solicitud")
    _get_entity_or_404(db, models.Usuario, "id_usuario", solicitud_cambio.id_usuario_solicita, "Usuario")
    if solicitud_cambio.id_usuario_objetivo is not None:
        _get_entity_or_404(db, models.Usuario, "id_usuario", solicitud_cambio.id_usuario_objetivo, "Usuario")
    if solicitud_cambio.id_revisor is not None:
        _get_entity_or_404(db, models.Usuario, "id_usuario", solicitud_cambio.id_revisor, "Usuario")

    db_solicitud = _get_entity_or_404(
        db, models.SolicitudCambio, "id_solicitud_cambio", id_solicitud_cambio, "Solicitud de cambio"
    )
    for field, value in solicitud_cambio.model_dump().items():
        setattr(db_solicitud, field, value)

    try:
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar solicitud de cambio: verifica usuarios, estado y consistencia del flujo.",
        )


def delete_solicitud_cambio(db: Session, id_solicitud_cambio: int):
    db_solicitud = _get_entity_or_404(
        db, models.SolicitudCambio, "id_solicitud_cambio", id_solicitud_cambio, "Solicitud de cambio"
    )
    _delete_entity(db, db_solicitud, "No se puede eliminar la solicitud de cambio porque está en uso.")
    return {"mensaje": "Solicitud de cambio eliminada correctamente."}

def get_certificaciones(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_solicitud: Optional[int] = None,
    dictamen: Optional[str] = None,
    fecha_certificacion_desde: Optional[datetime] = None,
    fecha_certificacion_hasta: Optional[datetime] = None,
):
    query = db.query(models.Certificacion)
    if id_solicitud is not None:
        query = query.filter(models.Certificacion.id_solicitud == id_solicitud)
    if dictamen:
        query = query.filter(models.Certificacion.dictamen == dictamen.strip().upper())
    if fecha_certificacion_desde is not None:
        query = query.filter(models.Certificacion.fecha_certificacion >= fecha_certificacion_desde)
    if fecha_certificacion_hasta is not None:
        query = query.filter(models.Certificacion.fecha_certificacion <= fecha_certificacion_hasta)
    return query.offset(skip).limit(limit).all()

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
def get_tipos_doc(db: Session, skip: int = 0, limit: int = 100, nombre: Optional[str] = None):
    query = db.query(models.TipoDoc)
    if nombre:
        query = query.filter(models.TipoDoc.nombre == nombre)
    return query.offset(skip).limit(limit).all()

def create_tipo_doc(db: Session, tipo_doc: schemas.TipoDocCreate):
    db_tipo_doc = models.TipoDoc(**tipo_doc.model_dump())
    db.add(db_tipo_doc)
    db.commit()
    db.refresh(db_tipo_doc)
    return db_tipo_doc

def get_requisitos_docs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_rol: Optional[int] = None,
    id_tipo_doc: Optional[int] = None,
    obligatorio: Optional[bool] = None,
):
    query = db.query(models.RequisitoDocRol)
    if id_rol is not None:
        query = query.filter(models.RequisitoDocRol.id_rol == id_rol)
    if id_tipo_doc is not None:
        query = query.filter(models.RequisitoDocRol.id_tipo_doc == id_tipo_doc)
    if obligatorio is not None:
        query = query.filter(models.RequisitoDocRol.obligatorio == obligatorio)
    return query.offset(skip).limit(limit).all()

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

def get_documentos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_animal: Optional[int] = None,
    id_usuario_subio: Optional[int] = None,
    id_validador: Optional[int] = None,
    id_estado: Optional[int] = None,
    id_tipo_doc: Optional[int] = None,
    fecha_subida_desde: Optional[datetime] = None,
    fecha_subida_hasta: Optional[datetime] = None,
):
    query = db.query(models.Documento)
    if id_animal is not None:
        query = query.filter(models.Documento.id_animal == id_animal)
    if id_usuario_subio is not None:
        query = query.filter(models.Documento.id_usuario_subio == id_usuario_subio)
    if id_validador is not None:
        query = query.filter(models.Documento.id_validador == id_validador)
    if id_estado is not None:
        query = query.filter(models.Documento.id_estado == id_estado)
    if id_tipo_doc is not None:
        query = query.filter(models.Documento.id_tipo_doc == id_tipo_doc)
    if fecha_subida_desde is not None:
        query = query.filter(models.Documento.fecha_subida >= fecha_subida_desde)
    if fecha_subida_hasta is not None:
        query = query.filter(models.Documento.fecha_subida <= fecha_subida_hasta)
    return query.offset(skip).limit(limit).all()

def create_documento(db: Session, documento: schemas.DocumentoCreate):
    _validate_estado_for_flow(db, documento.id_estado, "documento")
    _get_entity_or_404(db, models.Animal, "id_animal", documento.id_animal, "Animal")

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
            detail="Error al registrar documento: Verifica que el animal, usuario, estado y tipo de documento existan."
        )
    
# ==========================================
# CRUD PARA 'CATÁLOGOS GANADEROS'
# ==========================================
def get_categorias(db: Session, skip: int = 0, limit: int = 100, nombre: Optional[str] = None):
    query = db.query(models.CategoriaGanado)
    if nombre:
        query = query.filter(models.CategoriaGanado.nombre == nombre)
    return query.offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaGanadoCreate):
    db_cat = models.CategoriaGanado(**categoria.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_razas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_categoria: Optional[int] = None,
    nombre: Optional[str] = None,
):
    query = db.query(models.Raza)
    if id_categoria is not None:
        query = query.filter(models.Raza.id_categoria == id_categoria)
    if nombre:
        query = query.filter(models.Raza.nombre == nombre)
    return query.offset(skip).limit(limit).all()

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

def get_precios(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_categoria: Optional[int] = None,
    activo: Optional[bool] = None,
    fecha_vigencia_desde: Optional[datetime] = None,
    fecha_vigencia_hasta: Optional[datetime] = None,
):
    query = db.query(models.Precio)
    if id_categoria is not None:
        query = query.filter(models.Precio.id_categoria == id_categoria)
    if activo is not None:
        query = query.filter(models.Precio.activo == activo)
    if fecha_vigencia_desde is not None:
        query = query.filter(models.Precio.fecha_vigencia >= fecha_vigencia_desde)
    if fecha_vigencia_hasta is not None:
        query = query.filter(models.Precio.fecha_vigencia <= fecha_vigencia_hasta)
    return query.offset(skip).limit(limit).all()

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


def _get_entity_or_404(db: Session, model, id_field: str, id_value: int, label: str):
    entity = db.query(model).filter(getattr(model, id_field) == id_value).first()
    if not entity:
        raise HTTPException(status_code=404, detail=f"{label} no encontrado.")
    return entity


def _delete_entity(db: Session, entity, conflict_message: str):
    db.delete(entity)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=conflict_message)


# ==========================================
# UPDATE/DELETE PARA 'ESTADOS'
# ==========================================
def update_estado(db: Session, id_estado: int, estado: schemas.EstadoCreate):
    db_estado = _get_entity_or_404(db, models.Estado, "id_estado", id_estado, "Estado")
    existing_state = db.query(models.Estado).filter(
        models.Estado.nombre == estado.nombre,
        models.Estado.id_estado != id_estado,
    ).first()
    if existing_state:
        raise HTTPException(
            status_code=400,
            detail=f"El estado '{estado.nombre}' ya existe en el catálogo oficial.",
        )

    db_estado.nombre = estado.nombre
    db.commit()
    db.refresh(db_estado)
    return db_estado


def delete_estado(db: Session, id_estado: int):
    db_estado = _get_entity_or_404(db, models.Estado, "id_estado", id_estado, "Estado")
    _delete_entity(db, db_estado, "No se puede eliminar el estado porque está en uso.")
    return {"mensaje": "Estado eliminado correctamente."}


# ==========================================
# UPDATE/DELETE PARA 'ROLES'
# ==========================================
def update_rol(db: Session, id_rol: int, rol: schemas.RolCreate):
    db_rol = _get_entity_or_404(db, models.Rol, "id_rol", id_rol, "Rol")
    db_rol.nombre = rol.nombre
    db_rol.descripcion = rol.descripcion
    db.commit()
    db.refresh(db_rol)
    return db_rol


def delete_rol(db: Session, id_rol: int):
    db_rol = _get_entity_or_404(db, models.Rol, "id_rol", id_rol, "Rol")
    _delete_entity(db, db_rol, "No se puede eliminar el rol porque está en uso.")
    return {"mensaje": "Rol eliminado correctamente."}


# ==========================================
# UPDATE/DELETE PARA 'USUARIOS'
# ==========================================
def update_usuario(db: Session, id_usuario: int, usuario: schemas.UsuarioCreate):
    _validate_estado_for_flow(db, usuario.id_estado, "usuario")
    db_usuario = _get_entity_or_404(db, models.Usuario, "id_usuario", id_usuario, "Usuario")
    usuario_data = usuario.model_dump()
    usuario_data["password"] = get_password_hash(usuario.password)

    for field, value in usuario_data.items():
        setattr(db_usuario, field, value)

    try:
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar usuario: Verifica llaves foráneas y unicidad de usuario/email.",
        )


def delete_usuario(db: Session, id_usuario: int):
    db_usuario = _get_entity_or_404(db, models.Usuario, "id_usuario", id_usuario, "Usuario")
    _delete_entity(db, db_usuario, "No se puede eliminar el usuario porque está en uso.")
    return {"mensaje": "Usuario eliminado correctamente."}


# ==========================================
# UPDATE/DELETE PARA 'PRODUCTORES'
# ==========================================
def update_productor(db: Session, id_productor: int, productor: schemas.ProductorCreate):
    db_productor = _get_entity_or_404(db, models.Productor, "id_productor", id_productor, "Productor")
    for field, value in productor.model_dump().items():
        setattr(db_productor, field, value)

    try:
        db.commit()
        db.refresh(db_productor)
        return db_productor
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar productor: Verifica que el id_usuario sea válido y único.",
        )


def delete_productor(db: Session, id_productor: int):
    db_productor = _get_entity_or_404(db, models.Productor, "id_productor", id_productor, "Productor")
    _delete_entity(db, db_productor, "No se puede eliminar el productor porque está en uso.")
    return {"mensaje": "Productor eliminado correctamente."}


# ==========================================
# UPDATE/DELETE PARA 'ANIMALES'
# ==========================================
def update_animal(db: Session, id_animal: int, animal: schemas.AnimalCreate):
    _validate_estado_for_flow(db, animal.id_estado, "animal")
    db_animal = _get_entity_or_404(db, models.Animal, "id_animal", id_animal, "Animal")
    for field, value in animal.model_dump().items():
        setattr(db_animal, field, value)

    try:
        db.commit()
        db.refresh(db_animal)
        return db_animal
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar Animal: Verifica unicidad de arete y llaves foráneas.",
        )


def delete_animal(db: Session, id_animal: int):
    db_animal = _get_entity_or_404(db, models.Animal, "id_animal", id_animal, "Animal")
    _delete_entity(db, db_animal, "No se puede eliminar el animal porque está en uso.")
    return {"mensaje": "Animal eliminado correctamente."}


# ==========================================
# UPDATE/DELETE PARA 'DATOS VETERINARIOS'
# ==========================================
def update_veterinario(db: Session, id_docs_vet: int, veterinario: schemas.DatosVeterinariosCreate):
    db_veterinario = _get_entity_or_404(
        db, models.DatosVeterinarios, "id_docs_vet", id_docs_vet, "Datos veterinarios"
    )
    for field, value in veterinario.model_dump().items():
        setattr(db_veterinario, field, value)

    try:
        db.commit()
        db.refresh(db_veterinario)
        return db_veterinario
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar veterinario: Verifica que el id_usuario sea válido y único.",
        )


def delete_veterinario(db: Session, id_docs_vet: int):
    db_veterinario = _get_entity_or_404(
        db, models.DatosVeterinarios, "id_docs_vet", id_docs_vet, "Datos veterinarios"
    )
    _delete_entity(db, db_veterinario, "No se puede eliminar el veterinario porque está en uso.")
    return {"mensaje": "Datos veterinarios eliminados correctamente."}


# ==========================================
# UPDATE/DELETE PARA 'SOLICITUDES' Y 'CERTIFICACIONES'
# ==========================================
def update_solicitud(db: Session, id_solicitud: int, solicitud: schemas.SolicitudCertificacionCreate):
    _validate_estado_for_flow(db, solicitud.id_estado, "solicitud")
    db_solicitud = _get_entity_or_404(
        db, models.SolicitudCertificacion, "id_solicitud", id_solicitud, "Solicitud"
    )
    for field, value in solicitud.model_dump().items():
        setattr(db_solicitud, field, value)

    try:
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar solicitud: Verifica llaves foráneas y consistencia del flujo.",
        )


def delete_solicitud(db: Session, id_solicitud: int):
    db_solicitud = _get_entity_or_404(
        db, models.SolicitudCertificacion, "id_solicitud", id_solicitud, "Solicitud"
    )
    _delete_entity(db, db_solicitud, "No se puede eliminar la solicitud porque está en uso.")
    return {"mensaje": "Solicitud eliminada correctamente."}


def update_certificacion(db: Session, id_certificacion: int, certificacion: schemas.CertificacionCreate):
    db_certificacion = _get_entity_or_404(
        db, models.Certificacion, "id_certificacion", id_certificacion, "Certificación"
    )
    for field, value in certificacion.model_dump().items():
        setattr(db_certificacion, field, value)

    try:
        db.commit()
        db.refresh(db_certificacion)
        return db_certificacion
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar certificación: Verifica que la solicitud exista y sea válida.",
        )


def delete_certificacion(db: Session, id_certificacion: int):
    db_certificacion = _get_entity_or_404(
        db, models.Certificacion, "id_certificacion", id_certificacion, "Certificación"
    )
    _delete_entity(db, db_certificacion, "No se puede eliminar la certificación porque está en uso.")
    return {"mensaje": "Certificación eliminada correctamente."}


# ==========================================
# UPDATE/DELETE PARA 'GESTIÓN DOCUMENTAL'
# ==========================================
def update_tipo_doc(db: Session, id_tipo_doc: int, tipo_doc: schemas.TipoDocCreate):
    db_tipo_doc = _get_entity_or_404(db, models.TipoDoc, "id_tipo_doc", id_tipo_doc, "Tipo de documento")
    db_tipo_doc.nombre = tipo_doc.nombre
    db_tipo_doc.descripcion = tipo_doc.descripcion
    db.commit()
    db.refresh(db_tipo_doc)
    return db_tipo_doc


def delete_tipo_doc(db: Session, id_tipo_doc: int):
    db_tipo_doc = _get_entity_or_404(db, models.TipoDoc, "id_tipo_doc", id_tipo_doc, "Tipo de documento")
    _delete_entity(db, db_tipo_doc, "No se puede eliminar el tipo de documento porque está en uso.")
    return {"mensaje": "Tipo de documento eliminado correctamente."}


def update_requisito_doc(
    db: Session,
    id_rol: int,
    id_tipo_doc: int,
    requisito: schemas.RequisitoDocRolUpdate,
):
    db_requisito = db.query(models.RequisitoDocRol).filter(
        models.RequisitoDocRol.id_rol == id_rol,
        models.RequisitoDocRol.id_tipo_doc == id_tipo_doc,
    ).first()
    if not db_requisito:
        raise HTTPException(status_code=404, detail="Requisito documental no encontrado.")

    db_requisito.obligatorio = requisito.obligatorio
    db.commit()
    db.refresh(db_requisito)
    return db_requisito


def delete_requisito_doc(db: Session, id_rol: int, id_tipo_doc: int):
    db_requisito = db.query(models.RequisitoDocRol).filter(
        models.RequisitoDocRol.id_rol == id_rol,
        models.RequisitoDocRol.id_tipo_doc == id_tipo_doc,
    ).first()
    if not db_requisito:
        raise HTTPException(status_code=404, detail="Requisito documental no encontrado.")

    _delete_entity(db, db_requisito, "No se puede eliminar el requisito documental porque está en uso.")
    return {"mensaje": "Requisito documental eliminado correctamente."}


def update_documento(db: Session, id_doc_animal: int, documento: schemas.DocumentoCreate):
    _validate_estado_for_flow(db, documento.id_estado, "documento")
    _get_entity_or_404(db, models.Animal, "id_animal", documento.id_animal, "Animal")
    db_documento = _get_entity_or_404(db, models.Documento, "id_doc_animal", id_doc_animal, "Documento")
    for field, value in documento.model_dump().items():
        setattr(db_documento, field, value)

    try:
        db.commit()
        db.refresh(db_documento)
        return db_documento
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar documento: Verifica llaves foráneas y estado del flujo.",
        )


def delete_documento(db: Session, id_doc_animal: int):
    db_documento = _get_entity_or_404(db, models.Documento, "id_doc_animal", id_doc_animal, "Documento")
    _delete_entity(db, db_documento, "No se puede eliminar el documento porque está en uso.")
    return {"mensaje": "Documento eliminado correctamente."}


# ==========================================
# UPDATE/DELETE PARA 'CATÁLOGOS GANADEROS'
# ==========================================
def update_categoria(db: Session, id_categoria: int, categoria: schemas.CategoriaGanadoCreate):
    db_categoria = _get_entity_or_404(
        db, models.CategoriaGanado, "id_categoria", id_categoria, "Categoría"
    )
    db_categoria.nombre = categoria.nombre
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def delete_categoria(db: Session, id_categoria: int):
    db_categoria = _get_entity_or_404(
        db, models.CategoriaGanado, "id_categoria", id_categoria, "Categoría"
    )
    _delete_entity(db, db_categoria, "No se puede eliminar la categoría porque está en uso.")
    return {"mensaje": "Categoría eliminada correctamente."}


def update_raza(db: Session, id_raza: int, raza: schemas.RazaCreate):
    db_raza = _get_entity_or_404(db, models.Raza, "id_raza", id_raza, "Raza")
    for field, value in raza.model_dump().items():
        setattr(db_raza, field, value)

    try:
        db.commit()
        db.refresh(db_raza)
        return db_raza
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar raza: Verifica que el id_categoria exista.",
        )


def delete_raza(db: Session, id_raza: int):
    db_raza = _get_entity_or_404(db, models.Raza, "id_raza", id_raza, "Raza")
    _delete_entity(db, db_raza, "No se puede eliminar la raza porque está en uso.")
    return {"mensaje": "Raza eliminada correctamente."}


def update_precio(db: Session, id_precio: int, precio: schemas.PrecioCreate):
    db_precio = _get_entity_or_404(db, models.Precio, "id_precio", id_precio, "Precio")
    for field, value in precio.model_dump().items():
        setattr(db_precio, field, value)

    try:
        db.commit()
        db.refresh(db_precio)
        return db_precio
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar precio: Verifica que el id_categoria exista.",
        )


def delete_precio(db: Session, id_precio: int):
    db_precio = _get_entity_or_404(db, models.Precio, "id_precio", id_precio, "Precio")
    _delete_entity(db, db_precio, "No se puede eliminar el precio porque está en uso.")
    return {"mensaje": "Precio eliminado correctamente."}


# ==========================================
# CRUD/UPDATE/DELETE PARA 'ACCIONES'
# ==========================================
def get_acciones(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    nombre: Optional[str] = None,
):
    query = db.query(models.Accion)
    if nombre:
        query = query.filter(models.Accion.nombre == nombre)
    return query.offset(skip).limit(limit).all()


def create_accion(db: Session, accion: schemas.AccionCreate):
    db_accion = models.Accion(**accion.model_dump())
    db.add(db_accion)
    db.commit()
    db.refresh(db_accion)
    return db_accion


def update_accion(db: Session, id_accion: int, accion: schemas.AccionCreate):
    db_accion = _get_entity_or_404(db, models.Accion, "id_accion", id_accion, "Acción")
    db_accion.nombre = accion.nombre
    db_accion.descripcion = accion.descripcion
    db.commit()
    db.refresh(db_accion)
    return db_accion


def delete_accion(db: Session, id_accion: int):
    db_accion = _get_entity_or_404(db, models.Accion, "id_accion", id_accion, "Acción")
    _delete_entity(db, db_accion, "No se puede eliminar la acción porque está en uso.")
    return {"mensaje": "Acción eliminada correctamente."}


# ==========================================
# CRUD/UPDATE/DELETE PARA 'BITÁCORA'
# ==========================================
def get_bitacoras(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_usuario: Optional[int] = None,
    id_accion: Optional[int] = None,
    tabla_afectada: Optional[str] = None,
    fecha_cambio_desde: Optional[datetime] = None,
    fecha_cambio_hasta: Optional[datetime] = None,
):
    query = db.query(models.Bitacora)
    if id_usuario is not None:
        query = query.filter(models.Bitacora.id_usuario == id_usuario)
    if id_accion is not None:
        query = query.filter(models.Bitacora.id_accion == id_accion)
    if tabla_afectada:
        query = query.filter(models.Bitacora.tabla_afectada == tabla_afectada)
    if fecha_cambio_desde is not None:
        query = query.filter(models.Bitacora.fecha_cambio >= fecha_cambio_desde)
    if fecha_cambio_hasta is not None:
        query = query.filter(models.Bitacora.fecha_cambio <= fecha_cambio_hasta)
    return query.offset(skip).limit(limit).all()


def create_bitacora(db: Session, bitacora: schemas.BitacoraCreate):
    db_bitacora = models.Bitacora(**bitacora.model_dump())
    db.add(db_bitacora)
    try:
        db.commit()
        db.refresh(db_bitacora)
        return db_bitacora
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al registrar bitácora: Verifica que id_usuario e id_accion existan.",
        )


def update_bitacora(db: Session, id_bitacora: int, bitacora: schemas.BitacoraCreate):
    db_bitacora = _get_entity_or_404(db, models.Bitacora, "id_bitacora", id_bitacora, "Bitácora")
    for field, value in bitacora.model_dump().items():
        setattr(db_bitacora, field, value)

    try:
        db.commit()
        db.refresh(db_bitacora)
        return db_bitacora
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar bitácora: Verifica que id_usuario e id_accion existan.",
        )


def delete_bitacora(db: Session, id_bitacora: int):
    db_bitacora = _get_entity_or_404(db, models.Bitacora, "id_bitacora", id_bitacora, "Bitácora")
    _delete_entity(db, db_bitacora, "No se puede eliminar la bitácora porque está en uso.")
    return {"mensaje": "Bitácora eliminada correctamente."}


# ==========================================
# CRUD/UPDATE/DELETE PARA 'PRECIO_ANIMAL'
# ==========================================
def get_precios_animales(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_precio: Optional[int] = None,
    id_animal: Optional[int] = None,
    fecha_calculo_desde: Optional[datetime] = None,
    fecha_calculo_hasta: Optional[datetime] = None,
):
    query = db.query(models.PrecioAnimal)
    if id_precio is not None:
        query = query.filter(models.PrecioAnimal.id_precio == id_precio)
    if id_animal is not None:
        query = query.filter(models.PrecioAnimal.id_animal == id_animal)
    if fecha_calculo_desde is not None:
        query = query.filter(models.PrecioAnimal.fecha_calculo >= fecha_calculo_desde)
    if fecha_calculo_hasta is not None:
        query = query.filter(models.PrecioAnimal.fecha_calculo <= fecha_calculo_hasta)
    return query.offset(skip).limit(limit).all()


def create_precio_animal(db: Session, precio_animal: schemas.PrecioAnimalCreate):
    db_precio_animal = models.PrecioAnimal(**precio_animal.model_dump())
    db.add(db_precio_animal)
    try:
        db.commit()
        db.refresh(db_precio_animal)
        return db_precio_animal
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al registrar precio_animal: Verifica llaves foráneas y duplicados.",
        )


def update_precio_animal(
    db: Session,
    id_precio: int,
    id_animal: int,
    precio_animal: schemas.PrecioAnimalCreate,
):
    db_precio_animal = db.query(models.PrecioAnimal).filter(
        models.PrecioAnimal.id_precio == id_precio,
        models.PrecioAnimal.id_animal == id_animal,
    ).first()
    if not db_precio_animal:
        raise HTTPException(status_code=404, detail="PrecioAnimal no encontrado.")

    for field, value in precio_animal.model_dump().items():
        setattr(db_precio_animal, field, value)

    try:
        db.commit()
        db.refresh(db_precio_animal)
        return db_precio_animal
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar precio_animal: Verifica llaves foráneas y duplicados.",
        )


def delete_precio_animal(db: Session, id_precio: int, id_animal: int):
    db_precio_animal = db.query(models.PrecioAnimal).filter(
        models.PrecioAnimal.id_precio == id_precio,
        models.PrecioAnimal.id_animal == id_animal,
    ).first()
    if not db_precio_animal:
        raise HTTPException(status_code=404, detail="PrecioAnimal no encontrado.")

    _delete_entity(db, db_precio_animal, "No se puede eliminar el precio_animal porque está en uso.")
    return {"mensaje": "PrecioAnimal eliminado correctamente."}


# ==========================================
# CRUD/UPDATE/DELETE PARA 'ENFERMEDAD'
# ==========================================
def get_enfermedades(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    nombre: Optional[str] = None,
    requiere_cuarentena: Optional[bool] = None,
):
    query = db.query(models.Enfermedad)
    if nombre:
        query = query.filter(models.Enfermedad.nombre == nombre)
    if requiere_cuarentena is not None:
        query = query.filter(models.Enfermedad.requiere_cuarentena == requiere_cuarentena)
    return query.offset(skip).limit(limit).all()


def create_enfermedad(db: Session, enfermedad: schemas.EnfermedadCreate):
    db_enfermedad = models.Enfermedad(**enfermedad.model_dump())
    db.add(db_enfermedad)
    db.commit()
    db.refresh(db_enfermedad)
    return db_enfermedad


def update_enfermedad(db: Session, id_enfermedad: int, enfermedad: schemas.EnfermedadCreate):
    db_enfermedad = _get_entity_or_404(
        db,
        models.Enfermedad,
        "id_enfermedad",
        id_enfermedad,
        "Enfermedad",
    )
    db_enfermedad.nombre = enfermedad.nombre
    db_enfermedad.porcentaje_penalizacion = enfermedad.porcentaje_penalizacion
    db_enfermedad.requiere_cuarentena = enfermedad.requiere_cuarentena
    db.commit()
    db.refresh(db_enfermedad)
    return db_enfermedad


def delete_enfermedad(db: Session, id_enfermedad: int):
    db_enfermedad = _get_entity_or_404(
        db,
        models.Enfermedad,
        "id_enfermedad",
        id_enfermedad,
        "Enfermedad",
    )
    _delete_entity(db, db_enfermedad, "No se puede eliminar la enfermedad porque está en uso.")
    return {"mensaje": "Enfermedad eliminada correctamente."}


# ==========================================
# CRUD/UPDATE/DELETE PARA 'ENFERMEDAD_ANIMAL'
# ==========================================
def get_enfermedades_animales(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_enfermedad: Optional[int] = None,
    id_animal: Optional[int] = None,
    estado: Optional[str] = None,
    fecha_deteccion_desde: Optional[datetime] = None,
    fecha_deteccion_hasta: Optional[datetime] = None,
):
    query = db.query(models.EnfermedadAnimal)
    if id_enfermedad is not None:
        query = query.filter(models.EnfermedadAnimal.id_enfermedad == id_enfermedad)
    if id_animal is not None:
        query = query.filter(models.EnfermedadAnimal.id_animal == id_animal)
    if estado:
        query = query.filter(models.EnfermedadAnimal.estado == estado)
    if fecha_deteccion_desde is not None:
        query = query.filter(models.EnfermedadAnimal.fecha_deteccion >= fecha_deteccion_desde)
    if fecha_deteccion_hasta is not None:
        query = query.filter(models.EnfermedadAnimal.fecha_deteccion <= fecha_deteccion_hasta)
    return query.offset(skip).limit(limit).all()


def create_enfermedad_animal(db: Session, enfermedad_animal: schemas.EnfermedadAnimalCreate):
    db_enfermedad_animal = models.EnfermedadAnimal(**enfermedad_animal.model_dump())
    db.add(db_enfermedad_animal)
    try:
        db.commit()
        db.refresh(db_enfermedad_animal)
        return db_enfermedad_animal
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al registrar enfermedad_animal: Verifica llaves foráneas y duplicados.",
        )


def update_enfermedad_animal(
    db: Session,
    id_enfermedad: int,
    id_animal: int,
    enfermedad_animal: schemas.EnfermedadAnimalCreate,
):
    db_enfermedad_animal = db.query(models.EnfermedadAnimal).filter(
        models.EnfermedadAnimal.id_enfermedad == id_enfermedad,
        models.EnfermedadAnimal.id_animal == id_animal,
    ).first()
    if not db_enfermedad_animal:
        raise HTTPException(status_code=404, detail="EnfermedadAnimal no encontrada.")

    for field, value in enfermedad_animal.model_dump().items():
        setattr(db_enfermedad_animal, field, value)

    try:
        db.commit()
        db.refresh(db_enfermedad_animal)
        return db_enfermedad_animal
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar enfermedad_animal: Verifica llaves foráneas y duplicados.",
        )


def delete_enfermedad_animal(db: Session, id_enfermedad: int, id_animal: int):
    db_enfermedad_animal = db.query(models.EnfermedadAnimal).filter(
        models.EnfermedadAnimal.id_enfermedad == id_enfermedad,
        models.EnfermedadAnimal.id_animal == id_animal,
    ).first()
    if not db_enfermedad_animal:
        raise HTTPException(status_code=404, detail="EnfermedadAnimal no encontrada.")

    _delete_entity(db, db_enfermedad_animal, "No se puede eliminar la enfermedad_animal porque está en uso.")
    return {"mensaje": "EnfermedadAnimal eliminada correctamente."}

# Agrega esta función al final de crud.py
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.Usuario).filter(models.Usuario.usuario == username).first()
    if not user:
        return False
    
    # Comparamos la contraseña en texto plano contra el hash de la base de datos
    is_correct = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    if not is_correct:
        return False
        
    return user