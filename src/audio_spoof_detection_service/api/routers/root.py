from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import DishkaRoute

from audio_spoof_detection_service.api.schemas.root import RootResponse, CheckHealthResponse


root_router = APIRouter(route_class=DishkaRoute, prefix='', tags=['root'])


@root_router.get(
    path='/',
    responses={
        200: {'model': RootResponse}
    }
)
async def root() -> JSONResponse:
    response = RootResponse(
        message='Добро пожаловать в сервис определения синтезированных голосов в аудиофайлах!'
    )
    return JSONResponse(response.model_dump(mode='json'))


@root_router.get(
    path='/health',
    responses={
        200: {'model': CheckHealthResponse}
    }
)
async def check_health() -> JSONResponse:
    response = CheckHealthResponse(status='healthy')
    return JSONResponse(response.model_dump(mode='json'))
