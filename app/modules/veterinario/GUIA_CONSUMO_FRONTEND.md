# Guía de consumo de endpoints del veterinario

Esta guía resume cómo consumir los endpoints del módulo de veterinario desde el frontend.

## Reglas generales

- Todos los endpoints requieren autenticación con `Bearer token`.
- El backend valida que el usuario autenticado tenga `id_rol = 2`.
- La respuesta se entrega en JSON.
- Los filtros opcionales se envían como query params.
- Si el frontend usa un prefijo de API, agrega ese prefijo en la ruta base.

## Autenticación

En cada petición incluye el token:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

Ejemplo con `fetch`:

```js
const response = await fetch(`${API_BASE_URL}/perfil/`, {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
const data = await response.json();
```

## Endpoints del panel veterinario

### 1. Perfil del veterinario autenticado

Devuelve los datos personales y profesionales del veterinario logueado.

- Método: `GET`
- Ruta: `/perfil/`

Campos principales de respuesta:

- `nombre_completo`
- `email`
- `telefono`
- `ciudad`
- `estado_usuario`
- `fecha_registro`
- `cedula_profesional`
- `especialidad`
- `universidad`
- `total_certificaciones`

Ejemplo de respuesta:

```json
{
  "nombre_completo": "María Gómez López",
  "email": "maria@veterinaria.com",
  "telefono": "5559876543",
  "ciudad": "Zapopan",
  "estado_usuario": "Activo",
  "fecha_registro": "2026-08-08T12:30:00",
  "cedula_profesional": "CED-9876543",
  "especialidad": "Bovinos y Porcinos",
  "universidad": "UNAM",
  "total_certificaciones": 12
}
```

### 2. Solicitudes asignadas al veterinario

Lista las solicitudes de certificación asignadas al veterinario autenticado.

- Método: `GET`
- Ruta: `/solicitudes-panel/`
- Query params opcionales:
  - `id_estado`

Ejemplo:

```http
GET /solicitudes-panel/?id_estado=3
```

Campos principales de respuesta:

- `codigo_solicitud`
- `id_solicitud`
- `arete_animal`
- `tipo_ganado`
- `nombre_productor`
- `rancho`
- `raza`
- `edad_anios`
- `peso_est_kg`
- `fecha_solicitud`
- `estado_solicitud`

### 3. Bitácora personal del veterinario

Devuelve la actividad registrada del veterinario en la bitácora.

- Método: `GET`
- Ruta: `/bitacora/`

Ejemplo:

```http
GET /bitacora/
```

Campos principales de respuesta:

- `fecha_hora`
- `tipo_accion`
- `entidad_afectada`
- `detalles`

### 4. Documentos subidos por el veterinario

Lista los documentos que el veterinario subió al sistema.

- Método: `GET`
- Ruta: `/documentos-subidos/`

Ejemplo:

```http
GET /documentos-subidos/
```

Campos principales de respuesta:

- `nombre_documento`
- `enlace_documento`
- `estado_documento`
- `fecha_revision`

## Endpoints de gestión existentes

Además de las vistas de panel, el módulo conserva CRUD para mantenimiento o pantallas internas.

### Veterinarios

- `POST /veterinarios/`
- `GET /veterinarios/`
- `PUT /veterinarios/{id_docs_vet}`
- `DELETE /veterinarios/{id_docs_vet}`

### Solicitudes de certificación

- `POST /solicitudes/`
- `GET /solicitudes/`
- `PUT /solicitudes/{id_solicitud}`
- `DELETE /solicitudes/{id_solicitud}`

### Certificaciones

- `POST /certificaciones/`
- `GET /certificaciones/`
- `PUT /certificaciones/{id_certificacion}`
- `DELETE /certificaciones/{id_certificacion}`

## Recomendaciones para frontend

- Guarda el token después del login y reutilízalo en todo el panel.
- Maneja `403 Forbidden` como acceso denegado al panel de veterinario.
- Maneja `401 Unauthorized` como sesión expirada o token inválido.
- Para tablas grandes, usa filtros con query params antes de filtrar en cliente.
- Si la vista depende del usuario logueado, consume directamente `/perfil/` y no pases `id_usuario` desde el frontend.

## Ejemplo de helper

```js
export async function apiGet(path, token) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Error al consultar el backend');
  }

  return response.json();
}
```

## Nota importante

El backend valida el acceso del módulo veterinario con `id_rol = 2`.
