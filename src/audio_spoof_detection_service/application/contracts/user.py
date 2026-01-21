from dataclasses import dataclass

from audio_spoof_detection_service.domain.entities.user import UserEntity
from audio_spoof_detection_service.domain.types_and_consts import TokenPair


@dataclass(frozen=True)
class GetUserInfoInputDTO:
    email: str


@dataclass(frozen=True)
class GetUserInfoOutputDTO:
    result: UserEntity


@dataclass(frozen=True)
class RegisterUserInputDTO:
    username: str
    email: str


@dataclass(frozen=True)
class RegisterUserOutputDTO:
    result: UserEntity


@dataclass(frozen=True)
class LoginUserInputDTO:
    email: str
    one_time_password: str


@dataclass(frozen=True)
class LoginUserOutputDTO:
    result: TokenPair
