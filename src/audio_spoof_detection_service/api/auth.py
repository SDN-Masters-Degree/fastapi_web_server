from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dishka.integrations.fastapi import FromDishka, inject

from audio_spoof_detection_service.application.usecases.user import GetUserInfoUseCase
from audio_spoof_detection_service.application.contracts.user import GetUserInfoInputDTO, GetUserInfoOutputDTO


bearer_scheme = HTTPBearer()


@inject
async def get_current_user(
        get_user_info_interactor: FromDishka[GetUserInfoUseCase],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]
) -> GetUserInfoOutputDTO:
    try:
        access_token = credentials.credentials
        output = await get_user_info_interactor(GetUserInfoInputDTO(access_token=access_token))
        return output
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
