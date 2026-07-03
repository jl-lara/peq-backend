from app.database import SessionLocal
from app import models, crud
from datetime import datetime

def poblar_base_de_datos():
    db = SessionLocal()
    try:
        print("🌱 Iniciando el sembrado de datos (Seeding)...")

        # 1. Catálogos Base
        estado_activo = models.Estado(nombre="Activo")
        rol_productor = models.Rol(nombre="Productor", descripcion="Dueño del ganado")
        rol_vet = models.Rol(nombre="Veterinario", descripcion="Certificador oficial")
        cat_bovino = models.CategoriaGanado(nombre="Bovino")
        tipo_doc_ine = models.TipoDoc(nombre="Identificación Oficial", descripcion="INE o Pasaporte")
        
        db.add_all([estado_activo, rol_productor, rol_vet, cat_bovino, tipo_doc_ine])
        db.commit()

        # 2. Catálogos Dependientes
        raza_angus = models.Raza(id_categoria=cat_bovino.id_categoria, nombre="Angus", descripcion="Productora de carne")
        db.add(raza_angus)
        db.commit()

        # 3. Identidad y Perfiles (Usamos la función de crud para hashear la contraseña)
        password_hasheada = crud.get_password_hash("mi_password_seguro")
        
        user_juan = models.Usuario(
            nombre="Juan", apellido_paterno="Pérez", usuario="juan_productor",
            email="juan@rancho.com", telefono="5551234567", ciudad="Guadalajara",
            id_rol=rol_productor.id_rol, id_estado=estado_activo.id_estado, password=password_hasheada
        )
        user_maria = models.Usuario(
            nombre="María", apellido_paterno="Gómez", usuario="maria_vet",
            email="maria@veterinaria.com", telefono="5559876543", ciudad="Zapopan",
            id_rol=rol_vet.id_rol, id_estado=estado_activo.id_estado, password=password_hasheada
        )
        db.add_all([user_juan, user_maria])
        db.commit()

        prod_juan = models.Productor(
            id_usuario=user_juan.id_usuario, nombre="Rancho El Herradero",
            direccion="Km 15 Carretera Norte", capacidad_animales=500, superficie_hectareas=150.5
        )
        vet_maria = models.DatosVeterinarios(
            id_usuario=user_maria.id_usuario, cedula_profesional="CED-9876543",
            especialidad="Bovinos y Porcinos", universidad="UNAM"
        )
        db.add_all([prod_juan, vet_maria])
        db.commit()

        # 4. Registro Ganadero y Certificación
        animal_vaca = models.Animal(
            arete_id="MX-123456", id_productor=prod_juan.id_productor, id_raza=raza_angus.id_raza,
            id_estado=estado_activo.id_estado, sexo="M", edad=24, peso_kg=450.5, tiene_crias=False,
            proposito_produccion="Carne", condicion_general="Sano y con buen desarrollo"
        )
        db.add(animal_vaca)
        db.commit()

        solicitud = models.SolicitudCertificacion(
            id_estado=estado_activo.id_estado, id_animal=animal_vaca.id_animal, id_veterinario=user_maria.id_usuario
        )
        db.add(solicitud)
        db.commit()

        certificacion = models.Certificacion(
            id_solicitud=solicitud.id_solicitud, peso_validado=452.0,
            caracteristicas_validades="Cumple con el estándar racial Angus",
            observaciones_medicas="Vacunas al día", dictamen="Aprobado"
        )
        db.add(certificacion)
        db.commit()

        # 5. Gestión Documental
        documento = models.Documento(
            id_usuario_subio=user_juan.id_usuario, id_validador=user_maria.id_usuario,
            id_estado=estado_activo.id_estado, id_tipo_doc=tipo_doc_ine.id_tipo_doc,
            uri_archivo="https://mi-bucket.com/ine_juan.pdf", notas="Documento legible"
        )
        db.add(documento)
        db.commit()

        print("✅ ¡Éxito! La base de datos ha sido poblada con todos los datos de prueba.")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Ocurrió un error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    poblar_base_de_datos()