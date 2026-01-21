from fastapi import UploadFile
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from audio_spoof_detection_service.api.schemas.error import ErrorResponse
from audio_spoof_detection_service.api.schemas.audio import AudioResponse, AudioMetaInfo, AudioMetaInfoList
from audio_spoof_detection_service.application.usecases.audio import CheckAudioSpoofUseCase, GetAudioMetaInfosUseCase
from audio_spoof_detection_service.application.contracts.audio import CheckAudioSpoofInputDTO, GetAudioMetaInfosInputDTO


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
        CheckAudioSpoofInputDTO(
            audio_file=audio_file.file,
            audio_file_name=audio_file.filename
        )
    )
    return JSONResponse(AudioResponse(result=output.result).model_dump())


@audio_router.get(
    'analyze_results/user/{user_id}',
    responses={
        200: {'model': AudioMetaInfoList},
        404: {'model': ErrorResponse}
    }
)
async def get_users_all_audio_results(
        user_id: int,
        get_audio_meta_infos_interactor: FromDishka[GetAudioMetaInfosUseCase]
) -> JSONResponse:
    audio_meta_infos = await get_audio_meta_infos_interactor(GetAudioMetaInfosInputDTO(user_id=user_id))
    audio_meta_infos_schema = AudioMetaInfoList(
        audio_meta_infos=[
            AudioMetaInfo(
                id=audio_meta_info.id,
                name=audio_meta_info.name,
                analyze_result=audio_meta_info.analyze_result,
                created_at=audio_meta_info.created_at
            )
            for audio_meta_info in audio_meta_infos.result
        ]
    )
    return JSONResponse(audio_meta_infos_schema.model_dump())
