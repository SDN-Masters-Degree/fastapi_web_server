from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from audio_spoof_detection_service.api.routers.root import root_router
from audio_spoof_detection_service.api.routers.user import user_router
from audio_spoof_detection_service.api.routers.audio import audio_router
from audio_spoof_detection_service.api.exception_handler import domain_exception_handler
from audio_spoof_detection_service.domain.error import DomainError
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
    app.include_router(root_router)
    app.include_router(user_router)
    app.include_router(audio_router)


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_exception_handler)


def init_container(app: FastAPI) -> None:
    setup_dishka(create_container(), app)


def app_factory() -> FastAPI:
    app = FastAPI(
        title="Deepfake Voice Recognition",
        description="Сервис, определяющий дипфейки голосов",
        version="2026.01.26"
    )
    init_middleware(app)
    init_routers(app)
    init_exception_handlers(app)
    init_container(app)

    return app
