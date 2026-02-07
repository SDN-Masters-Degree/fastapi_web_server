from typing import Protocol

from audio_spoof_detection_service.domain.entities.user import UserEntity


class UserGateway(Protocol):
    async def register_user(self, user: UserEntity) -> UserEntity:
        raise NotImplementedError()

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        raise NotImplementedError()

    async def get_user_by_refresh_token(self, refresh_token: str) -> UserEntity | None:
        raise NotImplementedError()

    async def update_user(self, user: UserEntity) -> None:
        raise NotImplementedError()

    async def is_user_exists(self, email: str) -> bool:
        raise NotImplementedError()
