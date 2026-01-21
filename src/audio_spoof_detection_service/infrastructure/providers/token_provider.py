import secrets
from typing import Any
from datetime import datetime, timedelta

from jose import jwt

from audio_spoof_detection_service.application.protocols.providers.token_provider import TokenProvider
from audio_spoof_detection_service.infrastructure.settings import Settings
from audio_spoof_detection_service.domain.entities.user import UserEntity
from audio_spoof_detection_service.domain.types_and_consts import TokenPair


class JwtTokenProvider(TokenProvider):
    def __init__(self, settings: Settings):
        self.settings = settings

    async def generate_access_token(self, user: UserEntity) -> str:
        current_time = datetime.now()
        payload = {
            'sub': user.id,
            'username': user.name,
            'email': user.email,
            'type': 'access',
            'ait': current_time,
            'exp': current_time + timedelta(minutes=self.settings.access_token_expire_minutes)
        }
        return jwt.encode(payload, self.settings.jwt_secret_key, self.settings.algorithm)

    async def generate_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)

    async def verify_access_token(self, token: str) -> dict[str, Any] | None:
        payload = jwt.decode(token, self.settings.jwt_secret_key, self.settings.algorithm)

        if payload.get('type') != 'access':
            return None

        return payload

    async def create_token_pair(self, user: UserEntity) -> TokenPair:
        access_token = await self.generate_access_token(user)
        refresh_token = await self.generate_refresh_token()
        verified_token = await self.verify_access_token(access_token)
        return TokenPair(access_token=access_token, refresh_token=refresh_token, expires_at=verified_token.get('exp'))
