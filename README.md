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