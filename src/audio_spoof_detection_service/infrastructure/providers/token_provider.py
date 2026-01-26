from dataclasses import asdict
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from audio_spoof_detection_service.application.protocols.providers.token_provider import TokenProvider
from audio_spoof_detection_service.infrastructure.settings import Settings
from audio_spoof_detection_service.domain.entities.user import UserEntity
from audio_spoof_detection_service.domain.types_and_consts import TokenPayload


class JwtTokenProvider(TokenProvider):
    def __init__(self, settings: Settings):
        self.settings = settings

    async def generate_access_token(self, user: UserEntity) -> str:
        current_time = datetime.now(tz=timezone.utc)
        token_payload = TokenPayload(
            sub=user.email,
            type='access',
            exp=current_time + timedelta(minutes=self.settings.access_token_expire_minutes)
        )
        return jwt.encode(asdict(token_payload), self.settings.jwt_secret_key, self.settings.algorithm)

    async def generate_refresh_token(self, user: UserEntity) -> str:
        current_time = datetime.now(tz=timezone.utc)
        token_payload = TokenPayload(
            sub=user.email,
            type='refresh',
            exp=current_time + timedelta(days=self.settings.refresh_token_expire_days)
        )
        return jwt.encode(asdict(token_payload), self.settings.jwt_secret_key, self.settings.algorithm)

    async def verify_token(self, token: str) -> TokenPayload | None:
        try:
            payload = jwt.decode(token, self.settings.jwt_secret_key, self.settings.algorithm)

            if payload.get('type') in ('access', 'refresh'):
                return TokenPayload(**payload)

            return None
        except JWTError:
            return None
