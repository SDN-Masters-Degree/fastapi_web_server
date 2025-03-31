from fastapi import UploadFile
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from audio_spoof_detection_service.api.schemas.error import ErrorResponse
from audio_spoof_detection_service.api.schemas.audio import AudioResponse
from audio_spoof_detection_service.application.usecases.audio import CheckAudioSpoofUseCase
from audio_spoof_detection_service.application.contracts.audio import CheckAudioSpoofInputDTO


audio_router = APIRouter(route_class=DishkaRoute, prefix='/audio', tags=['Audio'])


@audio_router.post(
    '/check_spoof',
    responses={
        200: {'model': AudioResponse},
        404: {'model': ErrorResponse}
    }
)
async def check_spoof(
        audio_file: UploadFile,
        check_spoof_interactor: FromDishka[CheckAudioSpoofUseCase]
) -> JSONResponse:
    output = await check_spoof_interactor(
        CheckAudioSpoofInputDTO(audio_file=audio_file.file)
    )
    return JSONResponse(AudioResponse(result=output.result).model_dump())
