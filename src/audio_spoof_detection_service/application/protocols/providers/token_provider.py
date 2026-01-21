from typing import Protocol, Any

from audio_spoof_detection_service.domain.entities.user import UserEntity
from audio_spoof_detection_service.domain.types_and_consts import TokenPair


class TokenProvider(Protocol):
    async def generate_access_token(self, user: UserEntity) -> str:
        raise NotImplementedError()

    async def generate_refresh_token(self) -> str:
        raise NotImplementedError()

    async def verify_access_token(self, token: str) -> dict[str, Any] | None:
        raise NotImplementedError()

    async def create_token_pair(self, user: UserEntity) -> TokenPair:
        raise NotImplementedError()
