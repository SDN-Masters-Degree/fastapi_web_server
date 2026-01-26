from typing import Literal
from datetime import datetime
from dataclasses import dataclass
from enum import StrEnum


class AudioResult(StrEnum):
    real = 'real'
    fake = 'fake'


@dataclass(frozen=True)
class TokenPayload:
    sub: str
    type: Literal['access', 'refresh']
    exp: datetime
