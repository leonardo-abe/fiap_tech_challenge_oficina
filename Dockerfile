FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# instala as dependências antes de copiar o código da aplicação - camada de cache
# separada, que só é invalidada quando pyproject.toml/uv.lock mudam (não a cada alteração
# de código-fonte). --no-install-project instala só as dependências aqui; o projeto em
# si é instalado pelo uv sync de baixo, depois que o código-fonte chega - por isso essa
# linha sozinha é só a primeira metade do setup, não o resultado final.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev --no-build

COPY . .
RUN uv sync --frozen --no-dev --no-build


FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

# roda como usuário não-root - o container nunca precisa de privilégio de root em runtime
RUN useradd --create-home --shell /usr/sbin/nologin appuser

# só o que é necessário em runtime vem do builder - código de teste, documentação e
# ferramentas de relatório (que entravam via COPY . . de um build single-stage) não
# fazem parte da imagem final.
COPY --from=builder --chown=appuser:appuser /app/.venv ./.venv
COPY --from=builder --chown=appuser:appuser /app/app ./app
COPY --from=builder --chown=appuser:appuser /app/migrations ./migrations
COPY --from=builder --chown=appuser:appuser /app/alembic.ini ./
COPY --from=builder --chown=appuser:appuser /app/pyproject.toml /app/uv.lock ./

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run fastapi run app/main.py --host 0.0.0.0 --port 8000"]
