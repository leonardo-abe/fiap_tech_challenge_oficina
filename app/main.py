from fastapi import FastAPI

from app.shared.settings import settings

app = FastAPI(title=settings.app_name)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
