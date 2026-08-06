from fastapi import FastAPI

from app.presentation.api.v1.auth.router import router as auth_router
from app.presentation.api.v1.clientes.router import router as clientes_router
from app.presentation.api.v1.pecas.router import router as pecas_router
from app.presentation.api.v1.servicos.router import router as servicos_router
from app.presentation.api.v1.usuarios.router import router as usuarios_router
from app.presentation.api.v1.veiculos.router import router as veiculos_router
from app.presentation.exception_handlers import registrar_exception_handlers
from app.shared.settings import settings

app = FastAPI(title=settings.app_name)

registrar_exception_handlers(app)

app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(clientes_router)
app.include_router(veiculos_router)
app.include_router(servicos_router)
app.include_router(pecas_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
