from datetime import datetime

from app import crud, models
from app.database import SessionLocal


PASSWORD_DEMO = crud.get_password_hash("123456")


def get_or_create(db, model, defaults=None, **filters):
    instance = db.query(model).filter_by(**filters).first()
    if instance is not None:
        return instance

    params = dict(filters)
    if defaults:
        params.update(defaults)

    instance = model(**params)
    db.add(instance)
    db.flush()
    return instance


def seed_estados(db):
    return {
        "activo": get_or_create(db, models.Estado, nombre="Activo"),
        "inactivo": get_or_create(db, models.Estado, nombre="Inactivo"),
        "pendiente": get_or_create(db, models.Estado, nombre="Pendiente de Revisión"),
        "aprobado": get_or_create(db, models.Estado, nombre="Aprobado"),
        "rechazado": get_or_create(db, models.Estado, nombre="Rechazado"),
        "en_revision": get_or_create(db, models.Estado, nombre="En Revisión"),
        "bloqueado": get_or_create(db, models.Estado, nombre="Bloqueado"),
        "registrado": get_or_create(db, models.Estado, nombre="Registrado"),
        "certificado": get_or_create(db, models.Estado, nombre="Certificado"),
    }


def seed_roles(db):
    return {
        "vet": get_or_create(
            db,
            models.Rol,
            nombre="Veterinario",
            defaults={"descripcion": "Médico certificado encargado de validar el ganado y emitir los dictámenes."},
        ),
        "comercial": get_or_create(
            db,
            models.Rol,
            nombre="Productor Comercial",
            defaults={"descripcion": "Dueño de rancho establecido que comercializa ganado a gran escala."},
        ),
        "traspatio": get_or_create(
            db,
            models.Rol,
            nombre="Productor de Traspatio",
            defaults={"descripcion": "Pequeño productor rural."},
        ),
        "admin": get_or_create(
            db,
            models.Rol,
            id_rol=5,
            nombre="Administrador",
            defaults={"descripcion": "Acceso total al sistema. Gestiona catálogos, audita bitácoras y da soporte."},
        ),
    }


def seed_tipos_doc(db):
    return {
        "id_oficial": get_or_create(
            db,
            models.TipoDoc,
            nombre="Identificación Oficial",
            defaults={"descripcion": "Credencial para votar (INE), Pasaporte o Cartilla Militar."},
        ),
        "domicilio": get_or_create(
            db,
            models.TipoDoc,
            nombre="Comprobante de Domicilio",
            defaults={"descripcion": "Recibo de luz, agua o predial con vigencia no mayor a 3 meses."},
        ),
        "cedula": get_or_create(
            db,
            models.TipoDoc,
            nombre="Cédula Profesional",
            defaults={"descripcion": "Documento oficial expedido por la SEP para ejercer la medicina veterinaria."},
        ),
        "fiscal": get_or_create(
            db,
            models.TipoDoc,
            nombre="Constancia de Situación Fiscal",
            defaults={"descripcion": "Documento emitido por el SAT para facturación de Productores Comerciales."},
        ),
        "marca_herrar": get_or_create(
            db,
            models.TipoDoc,
            nombre="Título de Marca de Herrar",
            defaults={"descripcion": "Documento que avala la propiedad del fierro/marca del rancho ganadero."},
        ),
        "zoosanitario": get_or_create(
            db,
            models.TipoDoc,
            nombre="Certificado Zoosanitario",
            defaults={"descripcion": "Expedido por SENASICA, avala la salud general del hato ganadero."},
        ),
        "laboratorio": get_or_create(
            db,
            models.TipoDoc,
            nombre="Prueba de Laboratorio",
            defaults={"descripcion": "Resultados oficiales de pruebas de Brucelosis, Tuberculosis, etc."},
        ),
        "vacunacion": get_or_create(
            db,
            models.TipoDoc,
            nombre="Cartilla de Vacunación",
            defaults={"descripcion": "Registro de las dosis aplicadas al animal a lo largo de su vida."},
        ),
    }


def seed_categorias(db):
    return {
        "bovino": get_or_create(db, models.CategoriaGanado, nombre="Bovino"),
        "porcino": get_or_create(db, models.CategoriaGanado, nombre="Porcino"),
        "ovino": get_or_create(db, models.CategoriaGanado, nombre="Ovino"),
        "caprino": get_or_create(db, models.CategoriaGanado, nombre="Caprino"),
    }


def seed_acciones(db):
    return {
        "creado": get_or_create(db, models.Accion, nombre="Creado", defaults={"descripcion": "Registro generado"}),
        "actualizado": get_or_create(db, models.Accion, nombre="Actualizado", defaults={"descripcion": "Registro modificado"}),
        "eliminado": get_or_create(db, models.Accion, nombre="Eliminado", defaults={"descripcion": "Registro eliminado"}),
        "aprobado": get_or_create(db, models.Accion, nombre="Aprobado", defaults={"descripcion": "Registro aprobado"}),
        "rechazado": get_or_create(db, models.Accion, nombre="Rechazado", defaults={"descripcion": "Registro rechazado"}),
    }


def seed_enfermedades(db):
    return {
        "tuberculosis": get_or_create(db, models.Enfermedad, nombre="Tuberculosis Bovina", defaults={"porcentaje_penalizacion": 1.0, "requiere_cuarentena": True}),
        "brucelosis": get_or_create(db, models.Enfermedad, nombre="Brucelosis", defaults={"porcentaje_penalizacion": 1.0, "requiere_cuarentena": True}),
        "fiebre_porcida": get_or_create(db, models.Enfermedad, nombre="Fiebre Porcina Clásica", defaults={"porcentaje_penalizacion": 1.0, "requiere_cuarentena": True}),
        "mastitis": get_or_create(db, models.Enfermedad, nombre="Mastitis Clínica", defaults={"porcentaje_penalizacion": 0.15, "requiere_cuarentena": False}),
        "garrapatas": get_or_create(db, models.Enfermedad, nombre="Garrapatas (Infestación severa)", defaults={"porcentaje_penalizacion": 0.10, "requiere_cuarentena": False}),
        "gabarro": get_or_create(db, models.Enfermedad, nombre="Gabarro / Pedero", defaults={"porcentaje_penalizacion": 0.20, "requiere_cuarentena": True}),
        "prrs": get_or_create(db, models.Enfermedad, nombre="PRRS (Síndrome Reproductivo)", defaults={"porcentaje_penalizacion": 0.50, "requiere_cuarentena": True}),
        "parasitosis": get_or_create(db, models.Enfermedad, nombre="Parasitosis Gastrointestinal", defaults={"porcentaje_penalizacion": 0.05, "requiere_cuarentena": False}),
        "estomatitis": get_or_create(db, models.Enfermedad, nombre="Estomatitis Vesicular", defaults={"porcentaje_penalizacion": 0.80, "requiere_cuarentena": True}),
        "carbon": get_or_create(db, models.Enfermedad, nombre="Carbón Sintomático", defaults={"porcentaje_penalizacion": 1.0, "requiere_cuarentena": True}),
    }


def seed_razas(db, categorias):
    seeded = {}
    for categoria, nombre, descripcion in [
        (categorias["bovino"], "Angus", "Productora de carne de alta calidad, excelente marmoleo."),
        (categorias["bovino"], "Charolais", "Productora de carne, gran desarrollo muscular y rápida ganancia de peso."),
        (categorias["bovino"], "Holstein", "Principal raza productora de leche a nivel mundial."),
        (categorias["bovino"], "Brahman", "Alta resistencia al calor y garrapatas, excelente para cruzas de carne."),
        (categorias["bovino"], "Simmental", "Raza de doble propósito (carne y leche), gran adaptabilidad."),
        (categorias["bovino"], "Hereford", "Productora de carne, gran rusticidad y temperamento dócil."),
        (categorias["bovino"], "Jersey", "Productora de leche con alto contenido de grasa y proteína."),
        (categorias["porcino"], "Duroc", "Gran rusticidad, excelente calidad de carne e infiltración de grasa."),
        (categorias["porcino"], "Yorkshire", "Alta capacidad materna, gran tamaño y buena producción de carne."),
        (categorias["porcino"], "Pietrain", "Productora de carne muy magra, excelente desarrollo muscular."),
        (categorias["porcino"], "Landrace", "Cerdos largos con gran rendimiento en canal y habilidades maternas."),
        (categorias["porcino"], "Hampshire", "Excelente calidad de carne magra, adaptabilidad a pastoreo."),
        (categorias["ovino"], "Dorper", "Raza de pelo (no requiere esquila), excelente para producción de carne."),
        (categorias["ovino"], "Pelibuey", "Raza de pelo muy rústica y adaptada a climas cálidos, buena para carne."),
        (categorias["ovino"], "Suffolk", "Gran conformación cárnica, crecimiento rápido, cabeza y patas negras."),
        (categorias["ovino"], "Katahdin", "Raza de pelo de fácil mantenimiento, buena producción de carne."),
        (categorias["ovino"], "Rambouillet", "Raza de doble propósito, destacada por la calidad de su lana."),
        (categorias["caprino"], "Boer", "La mejor raza caprina para producción de carne, crecimiento rápido."),
        (categorias["caprino"], "Saanen", 'Excelente productora de leche, conocida como la "Holstein" de las cabras.'),
        (categorias["caprino"], "Alpina", "Gran productora de leche, muy rústica y adaptable a diferentes climas."),
        (categorias["caprino"], "Nubiana", "Doble propósito (carne y leche), alta resistencia al calor."),
        (categorias["caprino"], "Toggenburg", "Productora de leche, resistente a climas más fríos."),
    ]:
        key = f"{categoria.id_categoria}:{nombre}"
        seeded[key] = get_or_create(
            db,
            models.Raza,
            id_categoria=categoria.id_categoria,
            nombre=nombre,
            defaults={"descripcion": descripcion},
        )
    return seeded


def seed_usuarios(db, roles, estados):
    usuarios = {}
    usuarios["ana"] = get_or_create(
        db,
        models.Usuario,
        usuario="ana.torres",
        defaults={
            "nombre": "Ana",
            "apellido_paterno": "Torres",
            "apellido_materno": "López",
            "email": "ana.torres@sistema-ganado.gob.mx",
            "telefono": "6861234567",
            "ciudad": "Mexicali",
            "id_rol": roles["admin"].id_rol,
            "id_estado": estados["activo"].id_estado,
            "password": PASSWORD_DEMO,
        },
    )
    usuarios["luis"] = get_or_create(
        db,
        models.Usuario,
        usuario="luis.gomez",
        defaults={
            "nombre": "Luis",
            "apellido_paterno": "Gómez",
            "apellido_materno": "Sánchez",
            "email": "luis.gomez@sistema-ganado.gob.mx",
            "telefono": "6649876543",
            "ciudad": "Tijuana",
            "id_rol": roles["admin"].id_rol,
            "id_estado": estados["activo"].id_estado,
            "password": PASSWORD_DEMO,
        },
    )

    vet_data = [
        ("patricia.ruiz", "Patricia", "Ruiz", "Castro", "patricia.ruiz@email.com", "6461112233", "Ensenada", "BC-112233", "Medicina de Grandes Especies", "UABC"),
        ("roberto.medina", "Roberto", "Medina", "Silva", "roberto.medina@email.com", "6652223344", "Tecate", "BC-223344", "Zootecnia y Nutrición", "UABC"),
        ("carmen.vega", "Carmen", "Vega", "Ortiz", "carmen.vega@email.com", "6613334455", "Rosarito", "BC-334455", "Producción Caprina y Ovina", "UNAM"),
        ("jorge.ramos", "Jorge", "Ramos", "Díaz", "jorge.ramos@email.com", "6864445566", "Mexicali", "BC-445566", "Clínica de Rumiantes", "UABC"),
        ("silvia.nunez", "Silvia", "Núñez", "Flores", "silvia.nunez@email.com", "6645556677", "Tijuana", "BC-556677", "Calidad Cárnica", "UdeG"),
    ]
    for usuario, nombre, apellido_paterno, apellido_materno, email, telefono, ciudad, cedula, especialidad, universidad in vet_data:
        usuarios[usuario] = get_or_create(
            db,
            models.Usuario,
            usuario=usuario,
            defaults={
                "nombre": nombre,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "email": email,
                "telefono": telefono,
                "ciudad": ciudad,
                "id_rol": roles["vet"].id_rol,
                "id_estado": estados["activo"].id_estado,
                "password": PASSWORD_DEMO,
            },
        )

    producer_data = [
        ("miguel.castaneda", "Miguel", "Castañeda", "Ríos", "miguel.castaneda@email.com", "6866667788", "Mexicali", "Ganadera El Sol", "Carr. San Felipe Km 15, Mexicali", 1500, 400.5),
        ("fernando.herrera", "Fernando", "Herrera", "Cruz", "fernando.herrera@email.com", "6467778899", "Ensenada", "Rancho Ojos Negros", "Valle de Ojos Negros, Ensenada", 800, 250.0),
        ("laura.jimenez", "Laura", "Jiménez", "Mora", "laura.jimenez@email.com", "6658889900", "Tecate", "Establo Las Peñas", "Carr. Libre Tecate-Ensenada Km 20", 1200, 300.0),
        ("ricardo.vargas", "Ricardo", "Vargas", "Luna", "ricardo.vargas@email.com", "6649990011", "Tijuana", "Rancho El 2000", "Blvd. 2000 Sur, Tijuana", 600, 120.0),
        ("monica.aguilar", "Mónica", "Aguilar", "Pineda", "monica.aguilar@email.com", "6860001122", "Mexicali", "Engordas Mexicali", "Ejido Nuevo León, Mexicali", 2500, 600.0),
        ("hector.dominguez", "Héctor", "Domínguez", "Salas", "hector.dominguez@email.com", "6461112233", "Ensenada", "Rancho San Carlos", "Maneadero Parte Alta, Ensenada", 900, 200.0),
        ("teresa.suarez", "Teresa", "Suárez", "Nava", "teresa.suarez@email.com", "6612223344", "Rosarito", "Granja Familiar Suárez", "Cañón Histórico, Rosarito", 50, 2.5),
        ("javier.blanca", "Javier", "Blanca", "Soto", "javier.blanca@email.com", "6653334455", "Tecate", "El Cerrito", "Mixtlán, Tecate", 30, 1.0),
        ("rosa.morales", "Rosa", "Morales", "Vega", "rosa.morales@email.com", "6464445566", "Ensenada", "Traspatio Las Rosas", "San Antonio de las Minas, Ensenada", 40, 1.5),
        ("daniel.paredes", "Daniel", "Paredes", "León", "daniel.paredes@email.com", "6865556677", "Mexicali", "Parcela 14", "Ejido Puebla, Mexicali", 80, 5.0),
        ("beatriz.navarro", "Beatriz", "Navarro", "Gil", "beatriz.navarro@email.com", "6646667788", "Tijuana", "Granja La Esperanza", "Valle de las Palmas, Tijuana", 60, 3.0),
        ("arturo.campos", "Arturo", "Campos", "Peña", "arturo.campos@email.com", "6467778899", "Ensenada", "Rancho Chico", "Ejido Santo Tomás, Ensenada", 25, 0.8),
        ("elena.rosales", "Elena", "Rosales", "Mota", "elena.rosales@email.com", "6658889900", "Tecate", "Familia Rosales", "Nueva Colonia Hindú, Tecate", 45, 2.0),
    ]
    for usuario, nombre, apellido_paterno, apellido_materno, email, telefono, ciudad, nombre_rancho, direccion, capacidad, superficie in producer_data:
        usuarios[usuario] = get_or_create(
            db,
            models.Usuario,
            usuario=usuario,
            defaults={
                "nombre": nombre,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "email": email,
                "telefono": telefono,
                "ciudad": ciudad,
                "id_rol": roles["comercial"].id_rol if usuario in {"miguel.castaneda", "fernando.herrera", "laura.jimenez", "ricardo.vargas", "monica.aguilar", "hector.dominguez"} else roles["traspatio"].id_rol,
                "id_estado": estados["activo"].id_estado,
                "password": PASSWORD_DEMO,
            },
        )

    return usuarios


def seed_perfiles(db, usuarios, roles):
    vet_profiles = {
        "patricia.ruiz": {"cedula_profesional": "BC-112233", "especialidad": "Medicina de Grandes Especies", "universidad": "UABC"},
        "roberto.medina": {"cedula_profesional": "BC-223344", "especialidad": "Zootecnia y Nutrición", "universidad": "UABC"},
        "carmen.vega": {"cedula_profesional": "BC-334455", "especialidad": "Producción Caprina y Ovina", "universidad": "UNAM"},
        "jorge.ramos": {"cedula_profesional": "BC-445566", "especialidad": "Clínica de Rumiantes", "universidad": "UABC"},
        "silvia.nunez": {"cedula_profesional": "BC-556677", "especialidad": "Calidad Cárnica", "universidad": "UdeG"},
    }
    for usuario_key, data in vet_profiles.items():
        get_or_create(
            db,
            models.DatosVeterinarios,
            id_usuario=usuarios[usuario_key].id_usuario,
            defaults=data,
        )

    producer_profiles = {
        "miguel.castaneda": {"nombre": "Ganadera El Sol", "direccion": "Carr. San Felipe Km 15, Mexicali", "capacidad_animales": 1500, "superficie_hectareas": 400.5},
        "fernando.herrera": {"nombre": "Rancho Ojos Negros", "direccion": "Valle de Ojos Negros, Ensenada", "capacidad_animales": 800, "superficie_hectareas": 250.0},
        "laura.jimenez": {"nombre": "Establo Las Peñas", "direccion": "Carr. Libre Tecate-Ensenada Km 20", "capacidad_animales": 1200, "superficie_hectareas": 300.0},
        "ricardo.vargas": {"nombre": "Rancho El 2000", "direccion": "Blvd. 2000 Sur, Tijuana", "capacidad_animales": 600, "superficie_hectareas": 120.0},
        "monica.aguilar": {"nombre": "Engordas Mexicali", "direccion": "Ejido Nuevo León, Mexicali", "capacidad_animales": 2500, "superficie_hectareas": 600.0},
        "hector.dominguez": {"nombre": "Rancho San Carlos", "direccion": "Maneadero Parte Alta, Ensenada", "capacidad_animales": 900, "superficie_hectareas": 200.0},
        "teresa.suarez": {"nombre": "Granja Familiar Suárez", "direccion": "Cañón Histórico, Rosarito", "capacidad_animales": 50, "superficie_hectareas": 2.5},
        "javier.blanca": {"nombre": "El Cerrito", "direccion": "Mixtlán, Tecate", "capacidad_animales": 30, "superficie_hectareas": 1.0},
        "rosa.morales": {"nombre": "Traspatio Las Rosas", "direccion": "San Antonio de las Minas, Ensenada", "capacidad_animales": 40, "superficie_hectareas": 1.5},
        "daniel.paredes": {"nombre": "Parcela 14", "direccion": "Ejido Puebla, Mexicali", "capacidad_animales": 80, "superficie_hectareas": 5.0},
        "beatriz.navarro": {"nombre": "Granja La Esperanza", "direccion": "Valle de las Palmas, Tijuana", "capacidad_animales": 60, "superficie_hectareas": 3.0},
        "arturo.campos": {"nombre": "Rancho Chico", "direccion": "Ejido Santo Tomás, Ensenada", "capacidad_animales": 25, "superficie_hectareas": 0.8},
        "elena.rosales": {"nombre": "Familia Rosales", "direccion": "Nueva Colonia Hindú, Tecate", "capacidad_animales": 45, "superficie_hectareas": 2.0},
    }
    for usuario_key, data in producer_profiles.items():
        get_or_create(
            db,
            models.Productor,
            id_usuario=usuarios[usuario_key].id_usuario,
            defaults=data,
        )


def seed_catalogos_ganaderos(db, categorias):
    precio_bovino = get_or_create(
        db,
        models.Precio,
        id_categoria=categorias["bovino"].id_categoria,
        defaults={"precio_base_kilo": 68.5, "fecha_vigencia": datetime.utcnow(), "activo": True},
    )
    return {"precio_bovino": precio_bovino}


def seed_datos_operativos(db, usuarios, categorias, razas, estados, acciones, precios):
    producer = db.query(models.Productor).join(models.Usuario).filter(models.Usuario.usuario == "miguel.castaneda").first()
    veterinarian = db.query(models.DatosVeterinarios).join(models.Usuario).filter(models.Usuario.usuario == "patricia.ruiz").first()
    if producer and veterinarian:
        animal = get_or_create(
            db,
            models.Animal,
            arete_id="MX-123456",
            defaults={
                "id_productor": producer.id_productor,
                "id_raza": razas[f"{categorias['bovino'].id_categoria}:Angus"].id_raza,
                "id_estado": estados["certificado"].id_estado,
                "sexo": "M",
                "edad": 24,
                "peso_kg": 450.5,
                "tiene_crias": False,
                "proposito_produccion": "Carne",
                "condicion_general": "Sano y con buen desarrollo",
                "notas": "Ejemplar de prueba",
                "color_pelaje": "Negro",
                "estado_salud": "Sano",
                "foto_frontal": "https://mi-bucket.com/animal/frontal.jpg",
                "foto_lateral": "https://mi-bucket.com/animal/lateral.jpg",
            },
        )

        get_or_create(
            db,
            models.PrecioAnimal,
            id_precio=precios["precio_bovino"].id_precio,
            id_animal=animal.id_animal,
            defaults={
                "valor_agregado": 12.0,
                "modificador_porcentual": 3.0,
                "precio_base_aplicado": 68.5,
                "peso_al_calculo": 450.5,
                "precio_final": 83.0,
                "fecha_calculo": datetime.utcnow(),
            },
        )

        garrapata = db.query(models.Enfermedad).filter(models.Enfermedad.nombre == "Garrapatas (Infestación severa)").first()
        if garrapata:
            get_or_create(
                db,
                models.EnfermedadAnimal,
                id_enfermedad=garrapata.id_enfermedad,
                id_animal=animal.id_animal,
                defaults={"fecha_deteccion": datetime.utcnow(), "estado": "Activa"},
            )

        solicitud = get_or_create(
            db,
            models.SolicitudCertificacion,
            id_animal=animal.id_animal,
            defaults={
                "id_estado": estados["aprobado"].id_estado,
                "id_veterinario": usuarios["patricia.ruiz"].id_usuario,
                "fecha_revision": datetime.utcnow(),
                "fecha_dictamen": datetime.utcnow(),
            },
        )

        get_or_create(
            db,
            models.Certificacion,
            id_solicitud=solicitud.id_solicitud,
            defaults={
                "peso_validado": 452.0,
                "caracteristicas_validades": "Cumple con el estándar racial Angus",
                "observaciones_medicas": "Vacunas al día",
                "dictamen": "Aprobado",
                "fecha_certificacion": datetime.utcnow(),
            },
        )

        doc_ine = db.query(models.TipoDoc).filter(models.TipoDoc.nombre == "Identificación Oficial").first()
        if doc_ine:
            get_or_create(
                db,
                models.Documento,
                id_usuario_subio=usuarios["miguel.castaneda"].id_usuario,
                id_tipo_doc=doc_ine.id_tipo_doc,
                defaults={
                    "id_validador": usuarios["patricia.ruiz"].id_usuario,
                    "id_estado": estados["aprobado"].id_estado,
                    "url_archivo": "https://mi-bucket.com/ine_miguel.pdf",
                    "notas": "Documento legible",
                    "fecha_subida": datetime.utcnow(),
                    "fecha_revision": datetime.utcnow(),
                },
            )

        admin_user = usuarios["ana"]
        creado = acciones["creado"]
        actualizado = acciones["actualizado"]
        get_or_create(
            db,
            models.Bitacora,
            id_usuario=admin_user.id_usuario,
            id_accion=creado.id_accion,
            tabla_afectada="usuarios",
            defaults={"valor_anterior": None, "valor_nuevo": "Alta de usuarios base", "fecha_cambio": datetime.utcnow()},
        )
        get_or_create(
            db,
            models.Bitacora,
            id_usuario=admin_user.id_usuario,
            id_accion=actualizado.id_accion,
            tabla_afectada="documentos_animal",
            defaults={"valor_anterior": "Pendiente", "valor_nuevo": "Aprobado", "fecha_cambio": datetime.utcnow()},
        )


def poblar_base_de_datos():
    db = SessionLocal()
    try:
        print("🌱 Iniciando el sembrado de datos (Seeding)...")
        estados = seed_estados(db)
        roles = seed_roles(db)
        tipos_doc = seed_tipos_doc(db)
        categorias = seed_categorias(db)
        acciones = seed_acciones(db)
        enfermedades = seed_enfermedades(db)
        razas = seed_razas(db, categorias)
        usuarios = seed_usuarios(db, roles, estados)
        seed_perfiles(db, usuarios, roles)
        precios = seed_catalogos_ganaderos(db, categorias)
        seed_datos_operativos(db, usuarios, categorias, trazas, estados, acciones, precios)
        db.commit()
        print("✅ ¡Éxito! La base de datos ha sido poblada con los datos de referencia.")
    except Exception as e:
        db.rollback()
        print(f"❌ Ocurrió un error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    poblar_base_de_datos()