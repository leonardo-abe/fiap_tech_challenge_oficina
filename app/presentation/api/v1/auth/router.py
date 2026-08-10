from fastapi import APIRouter, Depends, Request, status

from app.infrastructure.security.rate_limiter import limiter
from app.presentation.api.v1.auth.controller import AuthController
from app.presentation.api.v1.auth.dependencies import get_auth_controller
from app.presentation.api.v1.auth.schemas import LoginRequestSchema, TokenResponseSchema

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def login(
    request: Request,
    dados: LoginRequestSchema,
    controller: AuthController = Depends(get_auth_controller),
) -> TokenResponseSchema:
    return await controller.login(dados)
