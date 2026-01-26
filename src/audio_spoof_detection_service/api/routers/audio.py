from fastapi import UploadFile, Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from audio_spoof_detection_service.api.schemas.error import ErrorResponse
from audio_spoof_detection_service.api.schemas.audio import AudioResponse, AudioMetaInfo, AudioMetaInfoList
from audio_spoof_detection_service.api.auth import get_current_user
from audio_spoof_detection_service.application.usecases.audio import CheckAudioSpoofUseCase, GetAudioMetaInfosUseCase
from audio_spoof_detection_service.application.contracts.user import GetUserInfoOutputDTO
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
        check_spoof_interactor: FromDishka[CheckAudioSpoofUseCase],
        get_user_interactor_result: GetUserInfoOutputDTO = Depends(get_current_user)
) -> JSONResponse:
    current_user = get_user_interactor_result.user
    output = await check_spoof_interactor(
        CheckAudioSpoofInputDTO(
            audio_file=audio_file.file,
            audio_file_name=audio_file.filename,
            user_id=current_user.id
        )
    )
    response = AudioResponse(result=output.result)
    return JSONResponse(response.model_dump(mode='json'))


@audio_router.get(
    '/analyze_results',
    responses={
        200: {'model': AudioMetaInfoList},
        404: {'model': ErrorResponse}
    }
)
async def get_users_all_audio_results(
        get_audio_meta_infos_interactor: FromDishka[GetAudioMetaInfosUseCase],
        get_user_interactor_result: GetUserInfoOutputDTO = Depends(get_current_user)
) -> JSONResponse:
    current_user = get_user_interactor_result.user
    audio_meta_infos = await get_audio_meta_infos_interactor(GetAudioMetaInfosInputDTO(user_id=current_user.id))
    response = AudioMetaInfoList(
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
    return JSONResponse(response.model_dump(mode='json'))
