# Guía de Integración Frontend-Backend (PeQ Backend)

> Estado: basada en el código actual del repositorio `jl-lara/peq-backend`.
> Objetivo: permitir que el equipo frontend comience implementación de forma inmediata.

---

## 1) Resumen de arquitectura y tecnologías

- **Framework API:** FastAPI (`/home/runner/work/peq-backend/peq-backend/app/main.py`)
- **Persistencia:** PostgreSQL + SQLAlchemy 2.0 (`/home/runner/work/peq-backend/peq-backend/app/database.py`, `/home/runner/work/peq-backend/peq-backend/app/models.py`)
- **Migraciones:** Alembic (`/home/runner/work/peq-backend/peq-backend/alembic/versions/ad01299e5362_creacion_inicial_postgres.py`)
- **Auth:** emisión de JWT en `/login` (`/home/runner/work/peq-backend/peq-backend/app/main.py`, `/home/runner/work/peq-backend/peq-backend/app/auth.py`)
- **Modelado de dominio:** usuarios/roles/estados, productores, animales, veterinarios, solicitudes/certificaciones, documentos, catálogos.

### Observación clave de seguridad funcional

Aunque existe endpoint de login y token JWT, **actualmente los endpoints de negocio no están protegidos por dependencia de auth** (no hay `OAuth2PasswordBearer` ni `get_current_user` aplicado en rutas).

---

## 2) Configuración para frontend

## URL base

- **Local (ejemplo):** `http://localhost:8000`
- **Producción:** `PENDIENTE_DEFINIR_POR_EQUIPO`  ← actualizar cuando compartan URL final

## Encabezados

- **Login:** `Content-Type: application/x-www-form-urlencoded`
- **Resto de endpoints:** `Content-Type: application/json`
- **Auth recomendada (futuro-compatible):** enviar header `Authorization` con esquema `Bearer` y el JWT de sesión.

## Versionado API

- No hay prefijo `/api/v1` en rutas actuales.
- Las rutas están expuestas en raíz (`/usuarios/`, `/animales/`, etc.).

## CORS

- No se encontró configuración de `CORSMiddleware` en `main.py`.
- Si frontend se despliega en otro dominio, se deberá habilitar CORS en backend.

---

## 3) Inventario completo de endpoints por módulo

> Nota: los `POST` devuelven 200 por defecto (no se configuró 201 explícito).  
> Todos los endpoints pueden devolver 422 por validación de request.

### 3.1 Health Check

| Método | Path | Propósito | Auth |
|---|---|---|---|
| GET | `/` | Salud del servicio | No |

### 3.2 Autenticación

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/login` | Obtiene JWT | No |

### 3.3 Catálogos - Estados

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/estados/` | Crear estado | No |
| GET | `/estados/` | Listar estados (`skip`, `limit`) | No |

### 3.4 Catálogos - Roles

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/roles/` | Crear rol | No |
| GET | `/roles/` | Listar roles (`skip`, `limit`) | No |

### 3.5 Usuarios

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/usuarios/` | Crear usuario | No |
| GET | `/usuarios/` | Listar usuarios (`skip`, `limit`) | No |

### 3.6 Productores

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/productores/` | Crear productor | No |
| GET | `/productores/` | Listar productores (`skip`, `limit`) | No |

### 3.7 Animales

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/animales/` | Crear animal | No |
| GET | `/animales/` | Listar animales (`skip`, `limit`) | No |

### 3.8 Flujo certificación (veterinarios)

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/veterinarios/` | Crear perfil veterinario | No |
| GET | `/veterinarios/` | Listar perfiles veterinarios (`skip`, `limit`) | No |

### 3.9 Flujo certificación (solicitudes)

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/solicitudes/` | Crear solicitud de certificación | No |
| GET | `/solicitudes/` | Listar solicitudes (`skip`, `limit`) | No |

### 3.10 Flujo certificación (certificaciones)

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/certificaciones/` | Emitir certificación | No |
| GET | `/certificaciones/` | Listar certificaciones (`skip`, `limit`) | No |

### 3.11 Gestión documental

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/tipos-documentos/` | Crear tipo de documento | No |
| GET | `/tipos-documentos/` | Listar tipos (`skip`, `limit`) | No |
| POST | `/requisitos-documentos/` | Crear requisito documental por rol | No |
| GET | `/requisitos-documentos/` | Listar requisitos (`skip`, `limit`) | No |
| POST | `/documentos/` | Crear registro documental | No |
| GET | `/documentos/` | Listar documentos (`skip`, `limit`) | No |

### 3.12 Catálogos ganaderos

| Método | Path | Propósito | Auth |
|---|---|---|---|
| POST | `/categorias-ganado/` | Crear categoría de ganado | No |
| GET | `/categorias-ganado/` | Listar categorías (`skip`, `limit`) | No |
| POST | `/razas/` | Crear raza | No |
| GET | `/razas/` | Listar razas (`skip`, `limit`) | No |
| POST | `/precios/` | Crear precio de mercado | No |
| GET | `/precios/` | Listar precios (`skip`, `limit`) | No |

---

## 4) Contratos por endpoint (request/response/errores)

## 4.1 Auth

### `POST /login`

- **Body:** `x-www-form-urlencoded`
  - `username: string`
  - `password: string`
- **Response 200:**
```json
{ "access_token": "jwt", "token_type": "bearer" }
```
- **Errores:**
  - `401` → `"Usuario o contraseña incorrectos"`

---

## 4.2 Entidades con patrón CRUD (POST + GET list)

Para todos los módulos siguientes:
- `GET` admite `skip` y `limit`.
- `GET` retorna array del esquema response.
- `POST` retorna objeto creado.
- `422` por validación.

### Estados
- Create: `{ nombre }`
- Response: `{ id_estado, nombre }`

### Roles
- Create: `{ nombre, descripcion? }`
- Response: `{ id_rol, nombre, descripcion? }`

### Usuarios
- Create:
```json
{
  "nombre": "string",
  "apellido_paterno": "string",
  "apellido_materno": "string|null",
  "usuario": "string",
  "email": "string",
  "telefono": "string|null",
  "ciudad": "string|null",
  "id_rol": 1,
  "id_estado": 1,
  "password": "string"
}
```
- Response: igual sin `password` + `id_usuario`
- Error 400 (integridad): rol/estado inexistente o usuario/email duplicado.

### Productores
- Create: `{ id_usuario, nombre, direccion?, capacidad_animales?, superficie_hectareas? }`
- Response: + `id_productor`
- Error 400: `id_usuario` inexistente o ya vinculado.

### Animales
- Create: `{ arete_id, id_productor, id_raza, id_estado, sexo, edad, peso_kg, tiene_crias, proposito_produccion, condicion_general? }`
- Response: + `id_animal`
- Error 400: `arete_id` duplicado o FKs inválidas.

### Veterinarios
- Create: `{ id_usuario, cedula_profesional, especialidad?, universidad? }`
- Response: + `id_docs_vet`
- Error 400: usuario inexistente o ya asignado como veterinario.

### Solicitudes de certificación
- Create: `{ id_estado, id_animal, id_veterinario?, fecha_revision?, fecha_dictamen? }`
- Response: + `id_solicitud`, `fecha_solicitud`
- Error 400: animal/estado/veterinario inválidos.

### Certificaciones
- Create: `{ id_solicitud, peso_validado, caracteristicas_validades, observaciones_medicas?, dictamen }`
- Response: + `id_certificacion`, `fecha_certificacion`
- Error 400: solicitud inexistente o solicitud ya certificada.

### Tipos de documentos
- Create: `{ nombre, descripcion? }`
- Response: + `id_tipo_doc`

### Requisitos documentales por rol
- Create: `{ id_rol, id_tipo_doc, obligatorio }`
- Response: mismo esquema
- Error 400: FKs inválidas o duplicado de llave compuesta (`id_rol` + `id_tipo_doc`).

### Documentos
- Create: `{ id_usuario_subio, id_validador?, id_estado, id_tipo_doc, uri_archivo, notas?, fecha_revision? }`
- Response: + `id_documento`
- Error 400: FKs inválidas.

### Categorías de ganado
- Create: `{ nombre }`
- Response: + `id_categoria`

### Razas
- Create: `{ id_categoria, nombre, descripcion? }`
- Response: + `id_raza`
- Error 400: categoría inválida.

### Precios
- Create: `{ id_categoria, precio_mercado }`
- Response: + `id_precio`
- Error 400: categoría inválida.

---

## 5) Flujos de UI/estado recomendados (frontend)

## 5.1 Flujo Auth

1. Pantalla login (form-data).
2. Si 200: guardar `access_token` (local storage/memory).
3. Si 401: error de credenciales.
4. Aunque hoy no sea obligatorio, enviar header `Authorization` para compatibilidad futura.

## 5.2 Flujo de carga de catálogos

1. Cargar `/estados/`, `/roles/`, `/categorias-ganado/`, `/razas/`, `/tipos-documentos/`.
2. Guardar en store local para combos.
3. Resolver dependencias (ej. razas por categoría) en UI.

## 5.3 Alta/edición operativa (sin update backend)

Secuencia sugerida:
1. Crear usuario.
2. Crear perfil productor o veterinario (según rol).
3. Crear animal (si rol productor).
4. Crear solicitud de certificación.
5. Crear certificación (si aplica).
6. Registrar documentos y requisitos.

## 5.4 Estados de proceso inferidos por datos

| Proceso | Criterio backend | Estado UI sugerido |
|---|---|---|
| Solicitud | `fecha_solicitud` existe | Creada |
| Solicitud | `fecha_revision` no nula | En revisión |
| Solicitud | `fecha_dictamen` no nula | Dictaminada |
| Certificación | existe registro certificación | Certificada |
| Documento | `id_validador` nulo/no nulo | Sin asignar / Asignado |
| Documento | `fecha_revision` no nula | Revisado |

> Para estados “Aprobado/Rechazado”, usar campo `dictamen` (texto libre) o catálogo `estados` según definición de negocio.

---

## 6) Matriz de errores backend → acción UI

| Código | Mensaje backend | Acción UI sugerida |
|---|---|---|
| 401 | Usuario o contraseña incorrectos | Mostrar error en login, no limpiar formulario completo |
| 400 | Error al registrar usuario... | Resaltar rol/estado, usuario/email duplicado |
| 400 | Error al registrar productor... | Validar usuario existente y no vinculado |
| 400 | Error al registrar Animal... | Validar arete único y FKs |
| 400 | Error al registrar veterinario... | Validar usuario y unicidad |
| 400 | Error al crear solicitud... | Validar animal/estado/veterinario |
| 400 | Error certificación solicitud... | Bloquear doble certificación |
| 400 | Error requisito documental... | Evitar duplicado rol+tipo |
| 400 | Error documento... | Validar usuario/estado/tipo doc |
| 422 | Validation error | Mostrar errores de campo |
| 500 | Error inesperado | Mensaje genérico + opción reintento |

---

## 7) Estrategia de cliente API (fetch/axios)

## 7.1 Cliente base con axios

```ts
import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000" // reemplazar por producción
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = "Bearer " + token;
  return config;
});
```

## 7.2 Login

```ts
export async function login(username: string, password: string) {
  const body = new URLSearchParams();
  body.append("username", username);
  body.append("password", password);

  const { data } = await api.post("/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  });

  localStorage.setItem("access_token", data.access_token);
  return data;
}
```

## 7.3 Ejemplo de alta animal

```ts
export async function crearAnimal(payload: {
  arete_id: string;
  id_productor: number;
  id_raza: number;
  id_estado: number;
  sexo: string;
  edad: number;
  peso_kg: number;
  tiene_crias: boolean;
  proposito_produccion: string;
  condicion_general?: string;
}) {
  const { data } = await api.post("/animales/", payload);
  return data;
}
```

---

## 8) Huecos/inconsistencias backend que impactan frontend

1. **Auth no aplicada a rutas de negocio** pese a existir login.
2. **Sin PUT/PATCH/DELETE**, por lo que no hay edición/baja API.
3. **Sin filtros por negocio**; solo paginación `skip/limit`.
4. **Sin endpoints para bitácora/acciones** aunque existen tablas de auditoría.
5. **Sin upload binario de archivos**; solo `uri_archivo`.
6. **Sin CORS explícito** para despliegue cross-domain.
7. **Estados de negocio no cerrados por enum**; dependen de catálogo parametrizable.

---

## 9) Preguntas abiertas para alinear con backend

1. ¿Cuáles son los valores oficiales de `estados` por flujo (solicitud/documento/animal/usuario)?
2. ¿`dictamen` debe limitarse a catálogo (Aprobado/Rechazado/Observado)?
3. ¿Qué endpoints deberán requerir auth obligatoria en producción?
4. ¿Se agregará versionado `/api/v1`?
5. ¿Habrá endpoints de actualización/cancelación?
6. ¿Se habilitará subida real de archivos (multipart)?
7. ¿Qué reglas regulatorias deben validarse en backend (rangos, transiciones, permisos por rol)?

---

## 10) Fuentes revisadas (código)

- `/home/runner/work/peq-backend/peq-backend/app/main.py`
- `/home/runner/work/peq-backend/peq-backend/app/schemas.py`
- `/home/runner/work/peq-backend/peq-backend/app/models.py`
- `/home/runner/work/peq-backend/peq-backend/app/crud.py`
- `/home/runner/work/peq-backend/peq-backend/app/auth.py`
- `/home/runner/work/peq-backend/peq-backend/app/database.py`
- `/home/runner/work/peq-backend/peq-backend/alembic/versions/ad01299e5362_creacion_inicial_postgres.py`
- `/home/runner/work/peq-backend/peq-backend/README.md`
