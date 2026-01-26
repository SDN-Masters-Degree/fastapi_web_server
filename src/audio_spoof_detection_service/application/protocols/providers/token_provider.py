from typing import Protocol

from audio_spoof_detection_service.domain.entities.user import UserEntity
from audio_spoof_detection_service.domain.types_and_consts import TokenPayload


class TokenProvider(Protocol):
    async def generate_access_token(self, user: UserEntity) -> str:
        raise NotImplementedError()

    async def generate_refresh_token(self, user: UserEntity) -> str:
        raise NotImplementedError()

    async def verify_token(self, token: str) -> TokenPayload | None:
        raise NotImplementedError()
