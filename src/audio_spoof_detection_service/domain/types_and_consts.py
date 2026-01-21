from datetime import datetime
from dataclasses import dataclass
from enum import StrEnum


class AudioResult(StrEnum):
    real = 'real'
    fake = 'fake'


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_at: datetime
