from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.audio import audio_router


def app_factory() -> FastAPI:
    app = FastAPI(title="Deepfake Voice Recognition",
                  description="Сервис, определяющий дипфейки голосов",
                  version="2024.10.08")

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"]
    )
    app.include_router(audio_router)

    return app
