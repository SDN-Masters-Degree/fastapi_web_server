from dataclasses import dataclass

from audio_spoof_detection_service.domain.entities.user import UserEntity


@dataclass(frozen=True)
class GetUserInfoInputDTO:
    access_token: str


@dataclass(frozen=True)
class GetUserInfoOutputDTO:
    user: UserEntity


@dataclass(frozen=True)
class RegisterUserInputDTO:
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class RegisterUserOutputDTO:
    user: UserEntity


@dataclass(frozen=True)
class LoginUserInputDTO:
    email: str
    password: str


@dataclass(frozen=True)
class LoginUserOutputDTO:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class LogoutUserInputDTO:
    refresh_token: str


@dataclass(frozen=True)
class LogoutUserOutputDTO:
    success: bool


@dataclass(frozen=True)
class RefreshUserTokensInputDTO:
    refresh_token: str


@dataclass(frozen=True)
class RefreshUserTokensOutputDTO:
    access_token: str
    refresh_token: str
