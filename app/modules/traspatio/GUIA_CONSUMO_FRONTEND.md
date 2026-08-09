# Guía de consumo de endpoints del módulo de traspatio

Esta guía resume cómo consumir el nuevo endpoint para consultar los animales registrados por el productor autenticado desde el frontend.

## Reglas generales

- Todos los endpoints requieren autenticación con Bearer token.
- El backend valida que el usuario autenticado tenga un perfil de productor asociado.
- La respuesta se entrega en JSON.
- Los filtros opcionales se envían como query params.
- Si tu frontend usa un prefijo de API, agrega ese prefijo en la ruta base.

## Autenticación

Incluye el token en cada petición:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

Ejemplo con fetch:

```js
const response = await fetch(`${API_BASE_URL}/traspatio/animales-productor/`, {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

const data = await response.json();
```

## Endpoint nuevo: animales registrados por el productor

### 1. Obtener animales del productor autenticado

- Método: `GET`
- Ruta: `/traspatio/animales-productor/`
- Query params opcionales:
  - `skip`
  - `limit`

Ejemplo:

```http
GET /traspatio/animales-productor/?skip=0&limit=20
```

### Campos de respuesta

Cada elemento de la respuesta contiene:

- `id_animal`
- `tipo_animal`
- `raza`
- `edad_anios`
- `peso_kg`
- `estado_certificacion`
- `precio_estimado`
- `fecha_registro`

### Ejemplo de respuesta

```json
[
  {
    "id_animal": 12,
    "tipo_animal": "Bovino",
    "raza": "Holstein",
    "edad_anios": 3,
    "peso_kg": 420.5,
    "estado_certificacion": "REGISTRADO",
    "precio_estimado": 1250.75,
    "fecha_registro": "2026-08-08T10:15:00"
  }
]
```

## Endpoints existentes del módulo de traspatio

### Perfil del productor autenticado

- Método: `GET`
- Ruta: `/traspatio/productor/`

### Animales del productor con filtros

- Método: `GET`
- Ruta: `/traspatio/animales/`
- Query params opcionales:
  - `skip`
  - `limit`
  - `id_raza`
  - `id_estado`
  - `sexo`
  - `edad_min`
  - `edad_max`
  - `peso_min`
  - `peso_max`
  - `arete_id`
  - `proposito_produccion`

### Documentos del productor

- Método: `GET`
- Ruta: `/traspatio/documentos/`
- Query params opcionales:
  - `skip`
  - `limit`
  - `id_estado`
  - `id_tipo_doc`
  - `fecha_subida_desde`
  - `fecha_subida_hasta`

### Solicitudes de certificación del productor

- Método: `GET`
- Ruta: `/traspatio/solicitudes/`
- Query params opcionales:
  - `skip`
  - `limit`
  - `id_estado`
  - `id_animal`
  - `id_veterinario`
  - `fecha_solicitud_desde`
  - `fecha_solicitud_hasta`

## Recomendaciones para frontend

- Usa `/traspatio/animales-productor/` para pantallas de dashboard o listas de animales del productor.
- Si necesitas más detalle de un animal, combina este endpoint con `/traspatio/animales/` o con el endpoint general de animales si el módulo lo expone en el futuro.
- Maneja `401 Unauthorized` como sesión expirada y `404` cuando el usuario no tiene perfil de productor.
- Para tablas grandes, usa `skip` y `limit` para paginar resultados.

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

El endpoint nuevo responde con datos resumidos del animal, pensados para paneles, listas y consumo ágil desde el frontend.
