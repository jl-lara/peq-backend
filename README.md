# PeQ - Plataforma de Gestión Ganadera (Backend API)

Bienvenido al repositorio del backend de **PeQ**. Esta API está construida con **FastAPI** y **PostgreSQL** para manejar la trazabilidad, gestión ganadera y certificación de animales.

## 🛠️ Stack Tecnológico
* **Framework:** FastAPI (Python)
* **Base de Datos:** PostgreSQL
* **ORM:** SQLAlchemy 2.0
* **Migraciones:** Alembic
* **Autenticación:** JWT (JSON Web Tokens)
* **Encriptación de contraseñas:** passlib (bcrypt)

---

## 💻 Guía para el Desarrollador Frontend

Toda la documentación interactiva de la API (endpoints, esquemas de datos y códigos de estado) se genera automáticamente gracias a Swagger. 

Una vez que el servidor esté corriendo, puedes ver y probar la API en:
👉 **URL de Documentación:** `http://localhost:8000/docs` (o la URL de producción una vez desplegado).

### Flujo de Autenticación (¡Importante!)
La API está protegida mediante Tokens JWT. Para interactuar con los endpoints seguros, debes seguir este flujo:

1. **Obtener el Token:** Realiza una petición `POST` al endpoint `/login`. 
   * **Atención:** Este endpoint espera los datos en formato `x-www-form-urlencoded` (Form Data), NO como un JSON crudo. Debes enviar `username` y `password`.
2. **Respuesta:** Si las credenciales son correctas, recibirás un JSON con el `access_token`.
3. **Peticiones Autenticadas:** Para consumir los demás endpoints (como crear animales o productores), debes incluir este token en los Headers de tu petición HTTP de la siguiente manera:
   ```http
   Authorization: Bearer <tu_access_token>

```

### Orden Lógico de Registro (Reglas de Negocio)

Debido a la integridad de la base de datos (Llaves Foráneas), el orden para crear un expediente ganadero es estricto:

1. Crear el `Usuario`.
2. Asignarle el rol de `Productor` (vinculado al ID del Usuario).
3. Registrar el `Animal` (vinculado al ID del Productor, ID de Raza e ID de Estado).
4. Generar la `Solicitud de Certificación` (vinculando al Animal y al Veterinario).

---

## 🚀 Guía de Despliegue en Render (Para Administración)

Este proyecto está configurado para ser desplegado fácilmente en **Render.com**. Sigue estos pasos para subir la API a producción:

### 1. Preparar el Repositorio

Asegúrate de que todo tu código esté en la rama `main` de tu repositorio de GitHub, incluyendo el archivo `requirements.txt`. **NUNCA subas el archivo `.env` al repositorio.**

### 2. Configurar el Web Service en Render

1. Entra a tu dashboard de Render y haz clic en **New +** -> **Web Service**.
2. Conecta tu cuenta de GitHub y selecciona el repositorio de `peq-backend`.
3. Configura el servicio con los siguientes datos:
* **Environment:** `Python 3`
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`



### 3. Variables de Entorno (Environment Variables)

En la configuración de Render, ve a la sección de "Environment" y agrega las variables que omitimos en GitHub (las que tenías en tu `.env` local):

* `DATABASE_URL`: `postgresql://tu_usuario:tu_password@ruta_interna_de_render/peq_db` *(Usa la "Internal Database URL" que te da Render en tu instancia de Postgres para mayor velocidad).*
* `SECRET_KEY`: `escribe_aqui_una_clave_secreta_muy_larga_y_segura`

### 4. Desplegar y Migrar

Haz clic en **Deploy**. Render instalará Python, las dependencias y arrancará `uvicorn`.

*(Nota: Como la base de datos ya fue migrada y construida previamente desde tu computadora local usando la URL externa con Alembic, Render simplemente se conectará a las tablas ya existentes. No necesitas correr Alembic desde Render a menos que modifiques la estructura de la base de datos en el futuro).*
