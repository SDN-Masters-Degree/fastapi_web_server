from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from audio_spoof_detection_service.api.routers.audio import audio_router
from audio_spoof_detection_service.api.exception_handler import (
    neural_model_exception_handler, audio_exception_handler
)
from audio_spoof_detection_service.domain.error import NeuralModelError, AudioError
from audio_spoof_detection_service.infrastructure.ioc import create_container


def init_middleware(app: FastAPI) -> None:
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"]
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(audio_router)


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NeuralModelError, neural_model_exception_handler)
    app.add_exception_handler(AudioError, audio_exception_handler)


def init_container(app: FastAPI) -> None:
    setup_dishka(create_container(), app)


def app_factory() -> FastAPI:
    app = FastAPI(
        title="Deepfake Voice Recognition",
        description="Сервис, определяющий дипфейки голосов",
        version="2025.05.07"
    )
    init_middleware(app)
    init_routers(app)
    init_exception_handlers(app)
    init_container(app)

    return app
