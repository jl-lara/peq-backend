from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app import models
from app.database import get_db

from . import crud, schemas



def require_admin_user(current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
	if current_user.id_rol is None:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="No tienes permisos para acceder al panel de administrador",
		)

	# Validamos por nombre de rol para no depender del ID sembrado en una BD concreta.
	rol = db.query(models.Rol).filter(models.Rol.id_rol == current_user.id_rol).first()

	if rol is None or rol.nombre.strip().upper() != "ADMINISTRADOR":
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="No tienes permisos para acceder al panel de administrador",
		)
	return current_user


router = APIRouter(dependencies=[Depends(require_admin_user)])


@router.post("/admin/usuarios/", response_model=schemas.UsuarioResponse, tags=["Gestión de Usuarios"])
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
	return crud.create_usuario(db=db, usuario=usuario)


@router.get("/admin/usuarios/", response_model=List[schemas.UsuarioResponse], tags=["Gestión de Usuarios"])
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
		db=db,
		skip=skip,
		limit=limit,
		id_rol=id_rol,
		id_estado=id_estado,
		ciudad=ciudad,
		usuario=usuario,
		email=email,
	)


@router.put("/admin/usuarios/{id_usuario}", response_model=schemas.UsuarioResponse, tags=["Gestión de Usuarios"])
def actualizar_usuario(id_usuario: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
	return crud.update_usuario(db=db, id_usuario=id_usuario, usuario=usuario)


@router.delete("/admin/usuarios/{id_usuario}", tags=["Gestión de Usuarios"])
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
	return crud.delete_usuario(db=db, id_usuario=id_usuario)


@router.get("/usuarios-activos/", response_model=List[schemas.ResumenUsuariosActivosResponse], tags=["Panel Administrador"])
def resumen_usuarios_activos(db: Session = Depends(get_db)):
	return crud.get_resumen_usuarios_activos_por_tipo(db=db)


@router.post("/admin/estados/", response_model=schemas.EstadoResponse, tags=["Catálogos Base"])
def crear_estado(estado: schemas.EstadoCreate, db: Session = Depends(get_db)):
	return crud.create_estado(db=db, estado=estado)


@router.get("/admin/estados/", response_model=List[schemas.EstadoResponse], tags=["Catálogos Base"])
def leer_estados(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
	return crud.get_estados(db=db, skip=skip, limit=limit, nombre=nombre)


@router.put("/admin/estados/{id_estado}", response_model=schemas.EstadoResponse, tags=["Catálogos Base"])
def actualizar_estado(id_estado: int, estado: schemas.EstadoCreate, db: Session = Depends(get_db)):
	return crud.update_estado(db=db, id_estado=id_estado, estado=estado)


@router.delete("/admin/estados/{id_estado}", tags=["Catálogos Base"])
def eliminar_estado(id_estado: int, db: Session = Depends(get_db)):
	return crud.delete_estado(db=db, id_estado=id_estado)


@router.post("/admin/roles/", response_model=schemas.RolResponse, tags=["Catálogos Base"])
def crear_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
	return crud.create_rol(db=db, rol=rol)


@router.get("/admin/roles/", response_model=List[schemas.RolResponse], tags=["Catálogos Base"])
def leer_roles(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
	return crud.get_roles(db=db, skip=skip, limit=limit, nombre=nombre)


@router.put("/admin/roles/{id_rol}", response_model=schemas.RolResponse, tags=["Catálogos Base"])
def actualizar_rol(id_rol: int, rol: schemas.RolCreate, db: Session = Depends(get_db)):
	return crud.update_rol(db=db, id_rol=id_rol, rol=rol)


@router.delete("/admin/roles/{id_rol}", tags=["Catálogos Base"])
def eliminar_rol(id_rol: int, db: Session = Depends(get_db)):
	return crud.delete_rol(db=db, id_rol=id_rol)


@router.post("/admin/acciones/", response_model=schemas.AccionResponse, tags=["Catálogos Base"])
def crear_accion(accion: schemas.AccionCreate, db: Session = Depends(get_db)):
	return crud.create_accion(db=db, accion=accion)


@router.get("/admin/acciones/", response_model=List[schemas.AccionResponse], tags=["Catálogos Base"])
def leer_acciones(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
	return crud.get_acciones(db=db, skip=skip, limit=limit, nombre=nombre)


@router.put("/admin/acciones/{id_accion}", response_model=schemas.AccionResponse, tags=["Catálogos Base"])
def actualizar_accion(id_accion: int, accion: schemas.AccionCreate, db: Session = Depends(get_db)):
	return crud.update_accion(db=db, id_accion=id_accion, accion=accion)


@router.delete("/admin/acciones/{id_accion}", tags=["Catálogos Base"])
def eliminar_accion(id_accion: int, db: Session = Depends(get_db)):
	return crud.delete_accion(db=db, id_accion=id_accion)


@router.get("/solicitudes-registro/", response_model=List[schemas.SolicitudRegistroAdminResponse], tags=["Panel Administrador"])
def leer_solicitudes_registro(
	id_estado: int | None = None,
	id_rol: int | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_solicitudes_registro_admin(db=db, id_estado=id_estado, id_rol=id_rol)


@router.get("/bitacora-sistema/", response_model=List[schemas.LogActividadAdminResponse], tags=["Panel Administrador"])
def leer_bitacora_sistema(
	id_usuario: int | None = None,
	id_rol: int | None = None,
	tabla_afectada: str | None = None,
	fecha_cambio_desde: datetime | None = None,
	fecha_cambio_hasta: datetime | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_bitacora_admin(
		db=db,
		id_usuario=id_usuario,
		id_rol=id_rol,
		tabla_afectada=tabla_afectada,
		fecha_cambio_desde=fecha_cambio_desde,
		fecha_cambio_hasta=fecha_cambio_hasta,
	)


@router.get("/documentos-revision/", response_model=List[schemas.DocumentoRevisionAdminResponse], tags=["Panel Administrador"])
def leer_documentos_revision(
	id_animal: int | None = None,
	id_usuario_subio: int | None = None,
	id_validador: int | None = None,
	id_estado: int | None = None,
	id_tipo_doc: int | None = None,
	fecha_subida_desde: datetime | None = None,
	fecha_subida_hasta: datetime | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_documentos_revision_admin(
		db=db,
		id_animal=id_animal,
		id_usuario_subio=id_usuario_subio,
		id_validador=id_validador,
		id_estado=id_estado,
		id_tipo_doc=id_tipo_doc,
		fecha_subida_desde=fecha_subida_desde,
		fecha_subida_hasta=fecha_subida_hasta,
	)


@router.get("/perfil-administrador/", response_model=schemas.PerfilAdministradorResponse, tags=["Panel Administrador"])
def leer_perfil_administrador(current_user=Depends(require_admin_user), db: Session = Depends(get_db)):
	perfil = crud.get_perfil_administrador(db=db, usuario_actual=current_user)
	if perfil is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el perfil del usuario autenticado")
	return perfil


@router.post("/tipos-documentos/", response_model=schemas.TipoDocResponse, tags=["Gestión Documental"])
def crear_tipo_doc(tipo_doc: schemas.TipoDocCreate, db: Session = Depends(get_db)):
	return crud.create_tipo_doc(db=db, tipo_doc=tipo_doc)


@router.get("/tipos-documentos/", response_model=List[schemas.TipoDocResponse], tags=["Gestión Documental"])
def leer_tipos_doc(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
	return crud.get_tipos_doc(db=db, skip=skip, limit=limit, nombre=nombre)


@router.put("/tipos-documentos/{id_tipo_doc}", response_model=schemas.TipoDocResponse, tags=["Gestión Documental"])
def actualizar_tipo_doc(id_tipo_doc: int, tipo_doc: schemas.TipoDocCreate, db: Session = Depends(get_db)):
	return crud.update_tipo_doc(db=db, id_tipo_doc=id_tipo_doc, tipo_doc=tipo_doc)


@router.delete("/tipos-documentos/{id_tipo_doc}", tags=["Gestión Documental"])
def eliminar_tipo_doc(id_tipo_doc: int, db: Session = Depends(get_db)):
	return crud.delete_tipo_doc(db=db, id_tipo_doc=id_tipo_doc)


@router.post("/requisitos-documentos/", response_model=schemas.RequisitoDocRolResponse, tags=["Gestión Documental"])
def crear_requisito_doc(requisito: schemas.RequisitoDocRolCreate, db: Session = Depends(get_db)):
	return crud.create_requisito_doc(db=db, requisito=requisito)


@router.get("/requisitos-documentos/", response_model=List[schemas.RequisitoDocRolResponse], tags=["Gestión Documental"])
def leer_requisitos_docs(
	skip: int = 0,
	limit: int = 100,
	id_rol: int | None = None,
	id_tipo_doc: int | None = None,
	obligatorio: bool | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_requisitos_docs(
		db=db,
		skip=skip,
		limit=limit,
		id_rol=id_rol,
		id_tipo_doc=id_tipo_doc,
		obligatorio=obligatorio,
	)


@router.put("/requisitos-documentos/{id_rol}/{id_tipo_doc}", response_model=schemas.RequisitoDocRolResponse, tags=["Gestión Documental"])
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


@router.delete("/requisitos-documentos/{id_rol}/{id_tipo_doc}", tags=["Gestión Documental"])
def eliminar_requisito_doc(id_rol: int, id_tipo_doc: int, db: Session = Depends(get_db)):
	return crud.delete_requisito_doc(db=db, id_rol=id_rol, id_tipo_doc=id_tipo_doc)


@router.post("/documentos/", response_model=schemas.DocumentoResponse, tags=["Gestión Documental"])
def crear_documento(documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
	return crud.create_documento(db=db, documento=documento)


@router.get("/documentos/", response_model=List[schemas.DocumentoResponse], tags=["Gestión Documental"])
def leer_documentos(
	skip: int = 0,
	limit: int = 100,
	id_animal: int | None = None,
	id_usuario_subio: int | None = None,
	id_validador: int | None = None,
	id_estado: int | None = None,
	id_tipo_doc: int | None = None,
	fecha_subida_desde: datetime | None = None,
	fecha_subida_hasta: datetime | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_documentos(
		db=db,
		skip=skip,
		limit=limit,
		id_animal=id_animal,
		id_usuario_subio=id_usuario_subio,
		id_validador=id_validador,
		id_estado=id_estado,
		id_tipo_doc=id_tipo_doc,
		fecha_subida_desde=fecha_subida_desde,
		fecha_subida_hasta=fecha_subida_hasta,
	)


@router.put("/documentos/{id_doc_animal}", response_model=schemas.DocumentoResponse, tags=["Gestión Documental"])
def actualizar_documento(id_doc_animal: int, documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
	return crud.update_documento(db=db, id_doc_animal=id_doc_animal, documento=documento)


@router.delete("/documentos/{id_doc_animal}", tags=["Gestión Documental"])
def eliminar_documento(id_doc_animal: int, db: Session = Depends(get_db)):
	return crud.delete_documento(db=db, id_doc_animal=id_doc_animal)


@router.post("/categorias-ganado/", response_model=schemas.CategoriaGanadoResponse, tags=["Catálogos Ganaderos"])
def crear_categoria(categoria: schemas.CategoriaGanadoCreate, db: Session = Depends(get_db)):
	return crud.create_categoria(db=db, categoria=categoria)


@router.get("/categorias-ganado/", response_model=List[schemas.CategoriaGanadoResponse], tags=["Catálogos Ganaderos"])
def leer_categorias(skip: int = 0, limit: int = 100, nombre: str | None = None, db: Session = Depends(get_db)):
	return crud.get_categorias(db=db, skip=skip, limit=limit, nombre=nombre)


@router.put("/categorias-ganado/{id_categoria}", response_model=schemas.CategoriaGanadoResponse, tags=["Catálogos Ganaderos"])
def actualizar_categoria(id_categoria: int, categoria: schemas.CategoriaGanadoCreate, db: Session = Depends(get_db)):
	return crud.update_categoria(db=db, id_categoria=id_categoria, categoria=categoria)


@router.delete("/categorias-ganado/{id_categoria}", tags=["Catálogos Ganaderos"])
def eliminar_categoria(id_categoria: int, db: Session = Depends(get_db)):
	return crud.delete_categoria(db=db, id_categoria=id_categoria)


@router.post("/razas/", response_model=schemas.RazaResponse, tags=["Catálogos Ganaderos"])
def crear_raza(raza: schemas.RazaCreate, db: Session = Depends(get_db)):
	return crud.create_raza(db=db, raza=raza)


@router.get("/razas/", response_model=List[schemas.RazaResponse], tags=["Catálogos Ganaderos"])
def leer_razas(
	skip: int = 0,
	limit: int = 100,
	id_categoria: int | None = None,
	nombre: str | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_razas(db=db, skip=skip, limit=limit, id_categoria=id_categoria, nombre=nombre)


@router.put("/razas/{id_raza}", response_model=schemas.RazaResponse, tags=["Catálogos Ganaderos"])
def actualizar_raza(id_raza: int, raza: schemas.RazaCreate, db: Session = Depends(get_db)):
	return crud.update_raza(db=db, id_raza=id_raza, raza=raza)


@router.delete("/razas/{id_raza}", tags=["Catálogos Ganaderos"])
def eliminar_raza(id_raza: int, db: Session = Depends(get_db)):
	return crud.delete_raza(db=db, id_raza=id_raza)


@router.post("/precios/", response_model=schemas.PrecioResponse, tags=["Catálogos Ganaderos"])
def crear_precio(precio: schemas.PrecioCreate, db: Session = Depends(get_db)):
	return crud.create_precio(db=db, precio=precio)


@router.get("/precios/", response_model=List[schemas.PrecioResponse], tags=["Catálogos Ganaderos"])
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
		db=db,
		skip=skip,
		limit=limit,
		id_categoria=id_categoria,
		activo=activo,
		fecha_vigencia_desde=fecha_vigencia_desde,
		fecha_vigencia_hasta=fecha_vigencia_hasta,
	)


@router.put("/precios/{id_precio}", response_model=schemas.PrecioResponse, tags=["Catálogos Ganaderos"])
def actualizar_precio(id_precio: int, precio: schemas.PrecioCreate, db: Session = Depends(get_db)):
	return crud.update_precio(db=db, id_precio=id_precio, precio=precio)


@router.delete("/precios/{id_precio}", tags=["Catálogos Ganaderos"])
def eliminar_precio(id_precio: int, db: Session = Depends(get_db)):
	return crud.delete_precio(db=db, id_precio=id_precio)


@router.post("/precios-animales/", response_model=schemas.PrecioAnimalResponse, tags=["Catálogos Ganaderos"])
def crear_precio_animal(precio_animal: schemas.PrecioAnimalCreate, db: Session = Depends(get_db)):
	return crud.create_precio_animal(db=db, precio_animal=precio_animal)


@router.get("/precios-animales/", response_model=List[schemas.PrecioAnimalResponse], tags=["Catálogos Ganaderos"])
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
		db=db,
		skip=skip,
		limit=limit,
		id_precio=id_precio,
		id_animal=id_animal,
		fecha_calculo_desde=fecha_calculo_desde,
		fecha_calculo_hasta=fecha_calculo_hasta,
	)


@router.put("/precios-animales/{id_precio}/{id_animal}", response_model=schemas.PrecioAnimalResponse, tags=["Catálogos Ganaderos"])
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


@router.delete("/precios-animales/{id_precio}/{id_animal}", tags=["Catálogos Ganaderos"])
def eliminar_precio_animal(id_precio: int, id_animal: int, db: Session = Depends(get_db)):
	return crud.delete_precio_animal(db=db, id_precio=id_precio, id_animal=id_animal)


@router.post("/bitacoras/", response_model=schemas.BitacoraResponse, tags=["Auditoría"])
def crear_bitacora(bitacora: schemas.BitacoraCreate, db: Session = Depends(get_db)):
	return crud.create_bitacora(db=db, bitacora=bitacora)


@router.get("/bitacoras/", response_model=List[schemas.BitacoraResponse], tags=["Auditoría"])
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
		db=db,
		skip=skip,
		limit=limit,
		id_usuario=id_usuario,
		id_accion=id_accion,
		tabla_afectada=tabla_afectada,
		fecha_cambio_desde=fecha_cambio_desde,
		fecha_cambio_hasta=fecha_cambio_hasta,
	)


@router.put("/bitacoras/{id_bitacora}", response_model=schemas.BitacoraResponse, tags=["Auditoría"])
def actualizar_bitacora(id_bitacora: int, bitacora: schemas.BitacoraCreate, db: Session = Depends(get_db)):
	return crud.update_bitacora(db=db, id_bitacora=id_bitacora, bitacora=bitacora)


@router.delete("/bitacoras/{id_bitacora}", tags=["Auditoría"])
def eliminar_bitacora(id_bitacora: int, db: Session = Depends(get_db)):
	return crud.delete_bitacora(db=db, id_bitacora=id_bitacora)


@router.post("/enfermedades/", response_model=schemas.EnfermedadResponse, tags=["Sanidad Animal"])
def crear_enfermedad(enfermedad: schemas.EnfermedadCreate, db: Session = Depends(get_db)):
	return crud.create_enfermedad(db=db, enfermedad=enfermedad)


@router.get("/enfermedades/", response_model=List[schemas.EnfermedadResponse], tags=["Sanidad Animal"])
def leer_enfermedades(
	skip: int = 0,
	limit: int = 100,
	nombre: str | None = None,
	requiere_cuarentena: bool | None = None,
	db: Session = Depends(get_db),
):
	return crud.get_enfermedades(
		db=db,
		skip=skip,
		limit=limit,
		nombre=nombre,
		requiere_cuarentena=requiere_cuarentena,
	)


@router.put("/enfermedades/{id_enfermedad}", response_model=schemas.EnfermedadResponse, tags=["Sanidad Animal"])
def actualizar_enfermedad(id_enfermedad: int, enfermedad: schemas.EnfermedadCreate, db: Session = Depends(get_db)):
	return crud.update_enfermedad(db=db, id_enfermedad=id_enfermedad, enfermedad=enfermedad)


@router.delete("/enfermedades/{id_enfermedad}", tags=["Sanidad Animal"])
def eliminar_enfermedad(id_enfermedad: int, db: Session = Depends(get_db)):
	return crud.delete_enfermedad(db=db, id_enfermedad=id_enfermedad)


@router.post("/enfermedades-animales/", response_model=schemas.EnfermedadAnimalResponse, tags=["Sanidad Animal"])
def crear_enfermedad_animal(enfermedad_animal: schemas.EnfermedadAnimalCreate, db: Session = Depends(get_db)):
	return crud.create_enfermedad_animal(db=db, enfermedad_animal=enfermedad_animal)


@router.get("/enfermedades-animales/", response_model=List[schemas.EnfermedadAnimalResponse], tags=["Sanidad Animal"])
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
		db=db,
		skip=skip,
		limit=limit,
		id_enfermedad=id_enfermedad,
		id_animal=id_animal,
		estado=estado,
		fecha_deteccion_desde=fecha_deteccion_desde,
		fecha_deteccion_hasta=fecha_deteccion_hasta,
	)


@router.put("/enfermedades-animales/{id_enfermedad}/{id_animal}", response_model=schemas.EnfermedadAnimalResponse, tags=["Sanidad Animal"])
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


@router.delete("/enfermedades-animales/{id_enfermedad}/{id_animal}", tags=["Sanidad Animal"])
def eliminar_enfermedad_animal(id_enfermedad: int, id_animal: int, db: Session = Depends(get_db)):
	return crud.delete_enfermedad_animal(db=db, id_enfermedad=id_enfermedad, id_animal=id_animal)
