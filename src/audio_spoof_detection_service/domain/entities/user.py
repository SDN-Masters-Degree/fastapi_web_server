from dataclasses import dataclass
from datetime import datetime

from audio_spoof_detection_service.domain.common.entity import Entity


@dataclass
class UserEntity(Entity):
    id: int | None
    name: str
    email: str
    refresh_token: str | None
    refresh_token_expires_at: datetime | None
    registered_at: datetime


@dataclass
class OneTimePasswordEntity(Entity):
    id: int
    user_id: int
    password: str
    expires_at: datetime
    is_active: bool
