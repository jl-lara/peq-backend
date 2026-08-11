# Guía de consumo de endpoints del administrador

Esta guía resume cómo consumir los endpoints del módulo de administrador desde el frontend.

## Reglas generales

- Todos los endpoints requieren autenticación con `Bearer token`.
- El backend valida que el usuario autenticado tenga `id_rol = 5`.
- La respuesta se entrega en JSON.
- Los filtros opcionales se envían como query params.
- Si tu frontend trabaja con una base URL prefijada como `/api`, agrega ese prefijo en las rutas.

## Autenticación

Incluye el token en cada petición:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

Ejemplo con `fetch`:

```js
const response = await fetch(`${API_BASE_URL}/usuarios-activos/`, {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
const data = await response.json();
```

## Endpoints disponibles

### 0. Gestión de usuarios

Este bloque cubre el mantenimiento de usuarios desde el panel de administración.

- `POST /admin/usuarios/`
- `GET /admin/usuarios/`
- `PUT /admin/usuarios/{id_usuario}`
- `DELETE /admin/usuarios/{id_usuario}`

Filtros disponibles en `GET /usuarios/`:

- `skip`
- `limit`
- `id_rol`
- `id_estado`
- `ciudad`
- `usuario`
- `email`

### 1. Resumen de usuarios activos por tipo

Obtiene el conteo de usuarios activos agrupados por rol.

- Método: `GET`
- Ruta: `/usuarios-activos/`
- Response: lista de objetos con `tipo_usuario` y `total_usuarios_activos`

Ejemplo de respuesta:

```json
[
  {
    "tipo_usuario": "Administrador",
    "total_usuarios_activos": 2
  },
  {
    "tipo_usuario": "Veterinario",
    "total_usuarios_activos": 5
  }
]
```

### 2. Solicitudes de registro

Lista usuarios registrados para revisión administrativa.

- Método: `GET`
- Ruta: `/solicitudes-registro/`
- Query params opcionales:
  - `id_estado`
  - `id_rol`

Ejemplo:

```http
GET /solicitudes-registro/?id_estado=3
```

Campos principales de respuesta:

- `id_usuario`
- `id_usuario_display`
- `nombre_completo`
- `tipo_rol`
- `email`
- `telefono`
- `fecha_solicitud`
- `estado_usuario`

### 3. Bitácora del sistema

Devuelve el historial de acciones registradas.

- Método: `GET`
- Ruta: `/bitacora-sistema/`
- Query params opcionales:
  - `id_usuario`
  - `id_rol`
  - `tabla_afectada`
  - `fecha_cambio_desde`
  - `fecha_cambio_hasta`

Ejemplo:

```http
GET /bitacora-sistema/?tabla_afectada=usuarios
```

Campos principales de respuesta:

- `fecha_hora`
- `usuario_responsable`
- `tipo_usuario`
- `accion`
- `entidad`
- `detalles`
- `ciudad`

### 4. Documentos en revisión

Muestra los documentos subidos por usuarios para aprobación o consulta.

- Método: `GET`
- Ruta: `/documentos-revision/`
- Query params opcionales:
  - `id_usuario_subio`
  - `id_validador`
  - `id_estado`
  - `id_tipo_doc`
  - `fecha_subida_desde`
  - `fecha_subida_hasta`

Ejemplo:

```http
GET /documentos-revision/?id_usuario_subio=12
```

Campos principales de respuesta:

- `id_doc_animal`
- `id_usuario_subio`
- `tipo_documento`
- `enlace_documento`

### 4.1 Subida de archivos

Para subir una imagen o documento antes de guardar la URL en la BD, usa:

- Ruta: `POST /media/subir/`
- Formato: `multipart/form-data`
- Campo requerido: `file`

La respuesta regresa la URL segura en `url` y `secure_url`. Esa URL se puede guardar en `documentos_animal.url_archivo` o en campos de imágenes de animal como `foto_frontal` y `foto_lateral`.
- `estado_revision`
- `notas_administrador`
- `fecha_revision`

### 4.1 Solicitudes de cambio

Este recurso permite crear, listar, editar y cancelar solicitudes de cambio.

- Método: `POST`
- Ruta: `/solicitudes-cambio/`
- Método: `GET`
- Ruta: `/solicitudes-cambio/`
- Método: `PUT`
- Ruta: `/solicitudes-cambio/{id_solicitud_cambio}`
- Método: `DELETE`
- Ruta: `/solicitudes-cambio/{id_solicitud_cambio}`

Campos del body:

- `id_usuario_solicita`
- `id_usuario_objetivo`
- `campo_afectado`
- `valor_anterior`
- `valor_nuevo`
- `motivo`
- `id_estado`
- `fecha_revision`
- `id_revisor`

Filtros opcionales en `GET`:

- `skip`
- `limit`
- `id_usuario_solicita`
- `id_usuario_objetivo`
- `id_revisor`
- `id_estado`
- `campo_afectado`
- `fecha_solicitud_desde`
- `fecha_solicitud_hasta`

Ejemplo de body:

```json
{
  "id_usuario_solicita": 12,
  "id_usuario_objetivo": 44,
  "campo_afectado": "estado_usuario",
  "valor_anterior": "Activo",
  "valor_nuevo": "Inactivo",
  "motivo": "Solicitud de cambio desde el panel",
  "id_estado": 3,
  "fecha_revision": null,
  "id_revisor": null
}
```

### 5. Perfil del administrador autenticado

Devuelve la información del usuario logueado.

- Método: `GET`
- Ruta: `/perfil-administrador/`

Ejemplo de respuesta:

```json
{
  "id_usuario": 1,
  "nombre_completo": "Ana Torres López",
  "email": "ana.torres@sistema-ganado.gob.mx",
  "telefono": "6861234567",
  "ciudad": "Mexicali",
  "rol_sistema": "Administrador",
  "miembro_desde": "2026-08-08T12:30:00",
  "estatus_cuenta": "Activo"
}
```

## Catálogos base

Estos catálogos ya están expuestos en el panel admin para que el frontend pueda administrarlos sin salir del módulo.

### Estados

- `POST /admin/estados/`
- `GET /admin/estados/`
- `PUT /admin/estados/{id_estado}`
- `DELETE /admin/estados/{id_estado}`

Filtro disponible en `GET /estados/`:

- `nombre`

Uso recomendado en frontend:

- Cargar el catálogo desde `GET /admin/estados/`.
- Usar `id_estado` en formularios, filtros y botones de acción.
- Evitar comparar por texto fijo, porque el backend valida por identificador y el nombre puede cambiar.

Ejemplo de consumo:

```js
const estados = await apiGet('/admin/estados/', token);
// estados.map((estado) => ({ label: estado.nombre, value: estado.id_estado }))
```

Prompt sugerido para la siguiente iteración del frontend:

- "Carga el catálogo de estados desde `GET /admin/estados/` y usa `id_estado` como valor real en selects, botones y filtros. No uses textos hardcodeados; solo muestra `nombre` en pantalla."

Estados sembrados actualmente en el backend:

- `Activo`
- `Inactivo`
- `Pendiente de Revisión`
- `En Revisión`
- `Aprobado`
- `Rechazado`
- `Bloqueado`
- `Registrado`
- `Certificado`

### Roles

- `POST /admin/roles/`
- `GET /admin/roles/`
- `PUT /admin/roles/{id_rol}`
- `DELETE /admin/roles/{id_rol}`

Filtro disponible en `GET /roles/`:

- `nombre`

### Acciones

- `POST /admin/acciones/`
- `GET /admin/acciones/`
- `PUT /admin/acciones/{id_accion}`
- `DELETE /admin/acciones/{id_accion}`

Filtro disponible en `GET /acciones/`:

- `nombre`

## Endpoints de gestión documental

Estos endpoints ya existen en el módulo admin y pueden ser útiles para pantallas de catálogo o configuración.

### Tipos de documentos

- `POST /tipos-documentos/`
- `GET /tipos-documentos/`
- `PUT /tipos-documentos/{id_tipo_doc}`
- `DELETE /tipos-documentos/{id_tipo_doc}`

### Requisitos de documentos por rol

- `POST /requisitos-documentos/`
- `GET /requisitos-documentos/`
- `PUT /requisitos-documentos/{id_rol}/{id_tipo_doc}`
- `DELETE /requisitos-documentos/{id_rol}/{id_tipo_doc}`

### Documentos

- `POST /documentos/`
- `GET /documentos/`
- `PUT /documentos/{id_doc_animal}`
- `DELETE /documentos/{id_doc_animal}`

## Endpoints de catálogos ganaderos

- `POST /categorias-ganado/`
- `GET /categorias-ganado/`
- `PUT /categorias-ganado/{id_categoria}`
- `DELETE /categorias-ganado/{id_categoria}`
- `POST /razas/`
- `GET /razas/`
- `PUT /razas/{id_raza}`
- `DELETE /razas/{id_raza}`
- `POST /precios/`
- `GET /precios/`
- `PUT /precios/{id_precio}`
- `DELETE /precios/{id_precio}`
- `POST /precios-animales/`
- `GET /precios-animales/`
- `PUT /precios-animales/{id_precio}/{id_animal}`
- `DELETE /precios-animales/{id_precio}/{id_animal}`

## Endpoints de administración de relaciones

### Requisitos de documentos por rol

- `POST /requisitos-documentos/`
- `GET /requisitos-documentos/`
- `PUT /requisitos-documentos/{id_rol}/{id_tipo_doc}`
- `DELETE /requisitos-documentos/{id_rol}/{id_tipo_doc}`

## Endpoints de auditoría y sanidad

- `POST /bitacoras/`
- `GET /bitacoras/`
- `PUT /bitacoras/{id_bitacora}`
- `DELETE /bitacoras/{id_bitacora}`
- `POST /enfermedades/`
- `GET /enfermedades/`
- `PUT /enfermedades/{id_enfermedad}`
- `DELETE /enfermedades/{id_enfermedad}`
- `POST /enfermedades-animales/`
- `GET /enfermedades-animales/`
- `PUT /enfermedades-animales/{id_enfermedad}/{id_animal}`
- `DELETE /enfermedades-animales/{id_enfermedad}/{id_animal}`

## Recomendaciones para frontend

- Centraliza la `API_BASE_URL` en un solo archivo.
- Reutiliza el token del login en un interceptor o helper HTTP.
- Maneja `403 Forbidden` como acceso denegado al panel admin.
- Maneja `401 Unauthorized` como sesión expirada o token inválido.
- Para pantallas de tabla, usa los filtros por query params en lugar de filtrar todo en cliente.

## Ejemplo de cliente reutilizable

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

El módulo admin está protegido por rol. Si el usuario autenticado no tiene `id_rol = 5`, el backend responderá `403`.
