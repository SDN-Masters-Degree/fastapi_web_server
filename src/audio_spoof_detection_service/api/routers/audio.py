from fastapi import UploadFile, Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from audio_spoof_detection_service.api.schemas.error import ErrorResponse
from audio_spoof_detection_service.api.schemas.audio import (
    AudioResponse, AudioMetaInfo, AudioMetaInfoList, DeleteAudioMetaInfoResponse
)
from audio_spoof_detection_service.api.auth import get_current_user
from audio_spoof_detection_service.application.usecases.audio import (
    CheckAudioSpoofUseCase, GetAudioMetaInfosUseCase, GetAudioMetaInfoUseCase, DeleteAudioMetaInfoUseCase
)
from audio_spoof_detection_service.application.contracts.user import GetUserInfoOutputDTO
from audio_spoof_detection_service.application.contracts.audio import (
    CheckAudioSpoofInputDTO, GetAudioMetaInfosInputDTO, GetAudioMetaInfoInputDTO, DeleteAudioMetaInfoInputDTO
)


audio_router = APIRouter(route_class=DishkaRoute, prefix='/audio', tags=['Audio'])


@audio_router.post(
    path='/check_spoof',
    responses={
        200: {'model': AudioResponse},
        404: {'model': ErrorResponse}
    }
)
async def check_spoof(
        audiofile: UploadFile,
        check_spoof_interactor: FromDishka[CheckAudioSpoofUseCase],
        get_user_interactor_result: GetUserInfoOutputDTO = Depends(get_current_user)
) -> JSONResponse:
    current_user = get_user_interactor_result.user
    output = await check_spoof_interactor(
        CheckAudioSpoofInputDTO(
            audiofile=audiofile.file,
            audiofile_name=audiofile.filename,
            user_id=current_user.id
        )
    )
    response = AudioResponse(result=output.result)
    return JSONResponse(response.model_dump(mode='json'))


@audio_router.get(
    path='/info',
    responses={
        200: {'model': AudioMetaInfoList},
        404: {'model': ErrorResponse}
    }
)
async def get_users_all_audio_infos(
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


@audio_router.get(
    path='/info/{audio_name}',
    responses={
        200: {'model': AudioMetaInfo},
        404: {'model': ErrorResponse}
    }
)
async def get_users_audio_info(
        audio_name: str,
        get_audio_meta_info_interactor: FromDishka[GetAudioMetaInfoUseCase],
        get_user_interactor_result: GetUserInfoOutputDTO = Depends(get_current_user)
) -> JSONResponse:
    current_user = get_user_interactor_result.user
    output = await get_audio_meta_info_interactor(
        GetAudioMetaInfoInputDTO(user_id=current_user.id, audiofile_name=audio_name)
    )
    response = AudioMetaInfo(
        id=output.audio_info.id,
        name=output.audio_info.name,
        analyze_result=output.audio_info.analyze_result,
        created_at=output.audio_info.created_at
    )
    return JSONResponse(response.model_dump(mode='json'))


@audio_router.delete(
    path='/info/{audio_name}',
    responses={
        200: {'model': AudioMetaInfo},
        404: {'model': ErrorResponse}
    }
)
async def delete_audio_info(
        audio_name: str,
        delete_audio_meta_info_interactor: FromDishka[DeleteAudioMetaInfoUseCase],
        get_user_interactor_result: GetUserInfoOutputDTO = Depends(get_current_user)
) -> JSONResponse:
    current_user = get_user_interactor_result.user
    output = await delete_audio_meta_info_interactor(
        DeleteAudioMetaInfoInputDTO(user_id=current_user.id, audiofile_name=audio_name)
    )
    response = DeleteAudioMetaInfoResponse(status=output.status)
    return JSONResponse(response.model_dump(mode='json'))
