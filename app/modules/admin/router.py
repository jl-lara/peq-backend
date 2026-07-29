from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import auth
from app.database import get_db

from . import crud, schemas

router = APIRouter(dependencies=[Depends(auth.get_current_user)])


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
