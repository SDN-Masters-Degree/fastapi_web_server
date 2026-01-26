from dataclasses import dataclass
from datetime import datetime

from audio_spoof_detection_service.domain.common.entity import Entity


@dataclass
class UserEntity(Entity):
    id: int | None
    name: str
    email: str
    hashed_password: str
    refresh_token: str | None
    registered_at: datetime
