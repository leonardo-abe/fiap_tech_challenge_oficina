from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.infrastructure.security.rate_limiter import limiter
from app.presentation.api.v1.auth.router import router as auth_router
from app.presentation.api.v1.clientes.router import router as clientes_router
from app.presentation.api.v1.ordens_servico.router import router as ordens_servico_router
from app.presentation.api.v1.pecas.router import router as pecas_router
from app.presentation.api.v1.servicos.router import router as servicos_router
from app.presentation.api.v1.usuarios.router import router as usuarios_router
from app.presentation.api.v1.veiculos.router import router as veiculos_router
from app.presentation.exception_handlers import registrar_exception_handlers
from app.shared.settings import settings

app = FastAPI(title=settings.app_name)

# limita força bruta em /auth/login e varredura sequencial na consulta pública de
# status de OS (únicas rotas sem JWT) - ver decorators @limiter.limit nesses routers.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

registrar_exception_handlers(app)

app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(clientes_router)
app.include_router(veiculos_router)
app.include_router(servicos_router)
app.include_router(pecas_router)
app.include_router(ordens_servico_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
