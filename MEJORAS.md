# PeQ Backend — Listado de Mejoras

Análisis del repositorio `peq-backend` (FastAPI + SQLAlchemy 2.0 + PostgreSQL + Alembic).

Las mejoras se agrupan por severidad/impacto: **Críticas**, **Seguridad**, **Arquitectura**, **Calidad de datos**, **API/UX** y **Despliegue**. Cada ítem incluye referencia al archivo y, cuando aplica, una solución sugerida.

---

## 1. Críticas (bugs que rompen flujo actual)

### 1.1 El script `seed.py` no ejecuta — NameError `trazas`
- `seed.py:468` pasa `trazas` a `seed_datos_operativos`, pero la variable se llama `razas`.
- Efecto: `python seed.py` lanza `NameError` y el sembrado nunca completa.
- Fix: `seed_datos_operativos(db, usuarios, categorias, razas, estados, acciones, precios)`.

### 1.2 Alembic tiene dos cabezas de migración — falla en despliegue limpio
- Cadenas detectadas con `alembic history`:
  - `ad0129... -> cf0c58... -> 1cce9a... -> 2f2947... -> 758e70... (head)`
  - `ad0129... -> cf0c58... -> 8b7d4c... (head)`
- Efecto: `alembic upgrade head` responde *"Multiple head revisions are present"*; en Render (README indica no correr migraciones, pero en cualquier BD nueva) no se puede migrar.
- Fix: crear una migración de merge (`alembic merge -m "merge heads" 758e7080ea32 8b7d4c1a2f6e`) o rebajar una de las ramas.

### 1.3 Migración vacía cometida
- `alembic/versions/2f294717da4d_crud_completo_validaciones.py` solo contiene `pass` (sin operaciones).
- Efecto: el historial promete cambios que no existen; confunde `alembic history` y diffs de `autogenerate`.
- Fix: borrarla (y regenerar con `alembic revision --autogenerate`) o completarla con su contenido real.

### 1.4 Funciones PostgreSQL no versionadas (dependencia oculta del backend)
- Endpoints dependen de funciones PL/pgSQL: `fn_obtener_panel_productor`, `fn_cambiar_password`, `fn_editar_perfil_productor`, `fn_obtener_perfil_veterinario`, `fn_actualizar_perfil_veterinario`, `fn_registrar_revision_veterinaria`, `fn_obtener_solicitudes_vet`, `fn_obtener_actividad_vet`, `fn_obtener_documentos_vet`.
- Estas funciones están en `BD/*.SQL`, pero `.gitignore:6` excluye `/BD` → **no se despliegan** con el repo. En Render/otro entorno los endpoints `/comercial/dashboard`, `/comercial/perfil/editar`, `/veterinario/*-db/`, etc. fallarán.
- Fix: versionar los scripts SQL (moverlos a `app/modules/*/` o `db/functions/`) y ejecutarlos vía Alembic (`op.execute`) o un paso de despliegue documentado.

### 1.5 Catálogo de estados del seed no coincide con el catálogo oficial de validación
- `app/schemas.py:7-13` define `OFFICIAL_STATES_BY_FLOW` (p.ej. `EN_REVISION`, `PENDIENTE`, `CERTIFICADO`).
- `seed.py:25-36` siembra nombres como `"En Revisión"`, `"Pendiente de Revisión"`, `"Registrado"`.
- `_validate_estado_for_flow` (`app/crud.py:25-38`) compara `nombre.strip().upper()` → `"EN REVISIÓN" != "EN_REVISION"`.
- Efecto: al crear/actualizar un Animal con el estado `En Revisión` sembrado, la API lo rechaza con 400 aunque el estado exista en BD.
- Fix: unificar nombres (siembra con los nombres oficiales exactos) o normalizar la comparación.

---

## 2. Seguridad (prioridad alta)

### 2.1 Escalada de privilegios: cualquier usuario autenticado administra usuarios y roles
- `app/modules/usuarios/router.py:12` crea `protected_router` solo con `Depends(auth.get_current_user)` y expone `POST /roles/`, `POST /usuarios/`, `DELETE /usuarios/` (líneas 15, 35, 69). **Cualquier usuario con token puede crearse un rol de administrador.**
- `app/modules/catalogos_base/router.py:10` igual para estados/acciones.
- Fix: mover estos CRUD al router de admin (`require_admin_user` en `app/modules/admin/router.py:15`) o crear un mecanismo RBAC centralizado reutilizable.

### 2.2 Sin validación de rol en módulos de productores
- `comercial/router.py:12` y `traspatio/router.py:12` solo exigen autenticación. Un veterinario o admin podría consumir endpoints de productor y, a la inversa, cualquier usuario lee `/comercial/*` y `/traspatio/*` de forma intercambiable.
- Fix: dependencias por rol (p.ej. `require_productor_comercial`, `require_productor_traspatio`) similares a `require_veterinario_user` / `require_admin_user`.

### 2.3 IDOR en ficha técnica de animales
- `GET /comercial/ficha-tecnica/{arete_id}` (`comercial/router.py:162`) y `GET /traspatio/ficha-tecnica/{arete_id}`: `get_ficha_tecnica_animal` (`comercial/crud.py:282`) consulta solo por `arete_id`, **sin verificar que el animal pertenezca al usuario autenticado**.
- Efecto: cualquier usuario autenticado puede leer ficha (dueño, teléfono, certificado, precios) de cualquier animal adivinando/recorriendo aretes.
- Fix: cruzar `id_productor` del usuario contra `animal.id_productor` antes de devolver la ficha.

### 2.4 Token JWT no valida el estado del usuario
- `auth.py:30-52` (`get_current_user`) no verifica `usuario.id_estado`. Un usuario `BLOQUEADO` o `INACTIVO` sigue operando con su token vigente.
- Fix: consultar el estado en cada request y rechazar con 403/401 si no está `ACTIVO`.

### 2.5 Login sin protección contra fuerza bruta
- `POST /login` (`usuarios/router.py:73`) no tiene rate-limit, bloqueo temporal ni backoff.
- Fix: limitador (slowapi/redis) o conteo de intentos fallidos por cuenta con bloqueo progresivo.

### 2.6 Fallback de contraseña en texto plano
- `verify_password` (`comercial/crud.py:353-365` y `traspatio/crud.py:356-368`) compara `plain_password == hashed_password` como respaldo. Si alguna cuenta quedó con contraseña en texto plano en BD, se normaliza una práctica insegura.
- Fix: eliminar el fallback y migrar a hashes bcrypt únicamente.

### 2.7 Fuga de errores internos en respuestas HTTP
- `comercial/crud.py:483-485` y `traspatio/crud.py:486-489` devuelven `detail=f"...: {str(err)}"` exponiendo detalles del motor de BD.
- Fix: devolver mensaje genérico y registrar el error interno con logging.

### 2.8 Gestión de tokens
- Solo `access_token` (30 min), sin refresh token ni revocación (`auth.py:18`). Para una plataforma gubernamental conviene un flujo refresh/revoke y, opcionalmente, reclamaciones mínimas en el JWT (actualmente incluye nombre y rol completos).
- `SECRET_KEY` se exige en import (bien), pero documentar rotación y no compartir entre ambientes.

---

## 3. Arquitectura y mantenibilidad

### 3.1 Duplicación casi total entre módulos comercial y traspatio
- `comercial/crud.py`, `comercial/router.py`, `traspatio/crud.py`, `traspatio/router.py` son prácticamente idénticos (productor, animales, documentos, solicitudes, actividades, perfil, dashboard, ficha técnica, contraseña).
- Fix: un módulo `productor` con rutas parametrizadas o una única implementación + alias de rutas; difiere únicamente el prefijo y, en el futuro, la lógica de negocio.

### 3.2 Monolito `app/crud.py` + adaptadores fantasma
- `app/crud.py` acumula 1217 líneas de CRUD para todas las entidades.
- `app/core/auth.py` y `app/core/database.py` son re-exportaciones (`from app.auth import *`) de compatibilidad; `app/modules/*/crud.py` en su mayoría solo delegan a `legacy_crud` (p.ej. `admin/crud.py`, `veterinario/crud.py`).
- Fix: eliminar shims de `app/core`, y migrar la lógica de cada módulo a su propio CRUD (el propio `app/modules/README.md:23-24` lo propone como siguiente paso).

### 3.3 Código muerto y duplicado dentro de archivos
- `comercial/crud.py:11` y `traspatio/crud.py:11`: `from passlib.context import CryptContext` sin uso.
- Re-imports a mitad de archivo: `import json` (`comercial/crud.py:415`, `traspatio/crud.py:418`), `HTTPException`/`text` (`comercial/crud.py:278-279`).
- Fix: limpiar imports al inicio y eliminar dependencias no usadas.

### 3.4 `requirements.txt` desordenado
- Duplicados al final: `passlib>=1.7.4` y `bcrypt>=4.0.1` repiten lo ya pineado en líneas 21 y 6.
- Dependencias aparentemente no usadas: `mysql-connector-python` (el proyecto es PostgreSQL), `geopy` (sin usos en `app/`), `Faker` (¿solo desarrollo?).
- Fix: separar `requirements.txt` (prod, pin exacto) y `requirements-dev.txt` (test/lint), y auditar paquetes con `pipreqs`/`pipdeptree`.

### 3.5 Sin pruebas automatizadas
- No existe `tests/` ni configuración de pytest para la app (solo librerías instaladas en venv).
- Fix: pytest + `fastapi.testclient` con BD de prueba (SQLite/Postgres efímero) cubriendo al menos: autenticación, validadores de dominio, flujo de certificación y los 3 roles.

### 3.6 Sin logging estructurado
- Uso de `print()` para errores (`app/crud.py:136`, `comercial/crud.py:409`).
- Fix: logging con `logger = logging.getLogger(__name__)`, niveles y formato JSON en producción; agregar `RequestIdMiddleware`.

### 3.7 Sin documentación de arquitectura actualizada
- README describe el flujo base pero no los paneles nuevos (admin, veterinario, traspatio) ni las rutas `/comercial/*`, `/veterinario/*`.
- Existen guías `GUIA_CONSUMO_FRONTEND.md` en algunos módulos (buena práctica); estandarizarlas en todas.

---

## 4. Calidad de datos y modelo

### 4.1 Fechas naive y API `datetime.utcnow()` deprecada
- `models.py` (10 usos) y `auth.py:25` usan `datetime.utcnow` (deprecado en Python 3.12) y guardan fechas sin zona horaria.
- Fix: `datetime.now(timezone.utc)` (o `DateTime(timezone=True)` + `ARRAY_TIMEZONE`) para consistencia multi-husos.

### 4.2 `token_qr` nunca se genera
- `Animal.token_qr` existe (`models.py:204`) pero ningún flujo lo crea ni hay endpoint público de verificación.
- Fix: generarlo al certificar (UUID/URL firmada) y exponer endpoint de consulta pública del certificado.

### 4.3 Números mágicos y valores hardcodeados en SQL crudo
- `ficha técnica`: `sc.id_estado = 4` (`comercial/crud.py:319`) asume el ID del estado APROBADO.
- `(u_prod.ciudad || ', Baja California')` (`comercial/crud.py:305`) hardcodea la entidad federativa.
- Fix: parametrizar por nombre de estado (`EN_REVISION`) y guardar estado/ubicación como datos, no literales.

### 4.4 Respuesta de dashboard sin normalizar
- `get_dashboard_productor` (`comercial/crud.py:262-275`) devuelve el `scalar()` de `fn_obtener_panel_productor`, que puede ser str JSON o dict, y solo como fallback devuelve la estructura esperada por `DashboardProductorResponse`.
- Fix: normalizar siempre (`json.loads` si es str) antes de retornar.

### 4.5 Borrado físico en contexto regulatorio
- `DELETE` de animales, certificaciones, documentos y bitácoras elimina registros definitivamente (`app/crud.py:654-657`, etc.). Para trazabilidad, un registro certificado no debería poder eliminarse en frío.
- Fix: soft delete (columna `activo`/`eliminado_at`) y auditoría previa en `bitacora`; bloquear borrado de animales certificados.

### 4.6 Validaciones de entrada insuficientes
- `UsuarioCreate.password` sin requisitos de fortaleza (`app/schemas.py:87`).
- `email` como `str` simple (usar `EmailStr`), `telefono` y `arete_id` sin patrón.
- `get_usuarios`/`create_usuario` no tratan unicidad case-insensitive de usuario/email.

### 4.7 Índices y restricciones
- Revisar índices para los filtros más usados (`animal.id_productor`, `documento.id_usuario_subio`, `bitacora.fecha_cambio`, `solicitudes_certificacion.id_veterinario`).
- Unicidad de `usuario`/`email` es case-sensitive por defecto.

---

## 5. API / UX

### 5.1 Paginación incompleta
- Todas las listas usan `skip/limit` sin total ni metadatos (`total`, `page`, `pages`).
- Fix: envolver respuestas paginadas o devolver `X-Total-Count`; definir límite máximo (p.ej. 100) y validación de `skip >= 0`.

### 5.2 Códigos de estado no diferenciados
- Conflictos de unicidad se responden como 400 genérico (p.ej. `app/crud.py:139-142`); debería ser 409 Conflict y 404 para no encontrado (ya hay `_get_entity_or_404`, pero no se usa de forma consistente en todo el CRUD).
- Error 500 por defecto sin handler global de excepciones → respuestas inconsistentes.

### 5.3 Sin versionado de API
- Todas las rutas cuelgan de `/`. Considerar `/api/v1/...` para evolución sin romper consumidores.

### 5.4 Consistencia de nombres de endpoints
- Existen pares duplicados por evolución (p.ej. `/perfil/` vs `/perfil-db/`, `/solicitudes-panel/` vs `/solicitudes-panel-db/`). Unificar y documentar cuál es la versión canónica.

### 5.5 Sin carga real de documentos
- `Documento.url_archivo` guarda solo un string URL; no hay endpoint `multipart/form-data` para subir archivos.
- Fix (según alcance): `UploadFile` + almacenamiento (S3/Disco) y validación de tipo/tamaño.

---

## 6. Despliegue y operación

### 6.1 Entorno local no reproducible
- No hay `Dockerfile` ni `docker-compose.yml` (Postgres + API). Solo `.venv` locales.
- Fix: compose con `postgres` + `uvicorn` + migración y seed automáticos.

### 6.2 README desactualizado
- Faltan: paneles (admin, veterinario, traspatio), variables de entorno actuales, pasos de migración (incluido el merge de cabezas) y ejecución del seed. La sección "Desplegar y Migrar" (README:90-94) asume BD preconstruida manualmente.

### 6.3 Pequeños desperfectos
- `alembic/env.py:13-14` y `:21` cargan `load_dotenv()` dos veces.
- `.gitignore` ignora `/BD` (relevante por el punto 1.4); añadir `.env.*`, `.pytest_cache/`, `.ruff_cache/` si se añaden herramientas.
- Documentar variables requeridas (`SECRET_KEY`, `DATABASE_URL`, `CORS_ALLOWED_ORIGINS`) en un `.env.example`.

---

## Resumen priorizado

| Prioridad | Ítems |
|---|---|
| **Alta (bugs/seguridad)** | 1.1, 1.2, 1.4, 2.1, 2.2, 2.3, 2.4 |
| **Media (arquitectura/datos)** | 1.3, 1.5, 2.5–2.8, 3.1–3.6, 4.1–4.5 |
| **Baja (calidad/UX/ops)** | 3.7, 4.6–4.7, 5.1–5.5, 6.1–6.3 |
