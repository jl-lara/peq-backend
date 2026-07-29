import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .modules.usuarios.router import (
    protected_router as usuarios_protected_router,
    public_router as usuarios_public_router,
)
from .modules.admin.router import router as admin_router
from .modules.catalogos_base.router import router as catalogos_base_router
from .modules.comercial.router import router as comercial_router
from .modules.traspatio.router import router as traspatio_router
from .modules.veterinario.router import router as veterinario_router

app = FastAPI(
    title="PeQ API - Gestión Ganadera",
    description="Backend para el sistema de trazabilidad y certificación PeQ.",
    version="1.0.0"
)

raw_cors_origins = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:4173",
)
cors_origins = [origin.strip() for origin in raw_cors_origins.split(",") if origin.strip()]
allow_credentials = "*" not in cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else ["http://localhost:3000"],
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "mensaje": "Bienvenido al Backend de PeQ"}

app.include_router(usuarios_protected_router)
app.include_router(usuarios_public_router)
app.include_router(catalogos_base_router)
app.include_router(comercial_router)
app.include_router(veterinario_router)
app.include_router(admin_router)
app.include_router(traspatio_router)