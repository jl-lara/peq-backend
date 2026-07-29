# Guia rapida de modulos

Objetivo: trabajar en paralelo sin conflictos de merge y sin romper el contrato actual de API.

## Reglas de trabajo

1. Cada equipo trabaja en su carpeta de modulo y evita editar `app/main.py` salvo para registrar su router.
2. Mantener rutas actuales durante la transicion (sin cambiar path ni payload en caliente).
3. Si un modulo requiere logica existente, usar adaptadores CRUD y migrar internamente por etapas.
4. Reutilizar componentes compartidos desde `app/core/` para auth y db.

## Estado actual de modularizacion

- `usuarios`: funcional (roles, usuarios y login)
- `catalogos_base`: funcional (estados y acciones)
- `comercial`: funcional (productores y animales)
- `veterinario`: funcional (veterinarios, solicitudes y certificaciones)
- `admin`: funcional (gestion documental, catalogos ganaderos, bitacora y sanidad)
- `traspatio`: funcional base (consultas propias de productor en `/traspatio/*`)

## Siguiente orden sugerido

1. Completar operaciones transaccionales de `traspatio` (crear/actualizar documentos y solicitudes del rol)
2. Reduccion de dependencia a `app/crud.py` moviendo logica desde adaptadores a CRUD nativo de cada modulo
3. Organizar pruebas por modulo para asegurar regresiones cero durante la transicion
