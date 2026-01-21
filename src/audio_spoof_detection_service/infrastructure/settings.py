import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()

DB_URL = 'DB_URL'
JWT_SECRET_KEY='JWT_SECRET_KEY'
JWT_REFRESH_SECRET_KEY='JWT_REFRESH_SECRET_KEY'
ALGORITHM='ALGORITHM'
ACCESS_TOKEN_EXPIRE_MINUTES='ACCESS_TOKEN_EXPIRE_MINUTES'
REFRESH_TOKEN_EXPIRE_DAYS='REFRESH_TOKEN_EXPIRE_DAYS'
SAMPLE_RATE = 'TARGET_SAMPLE_RATE'
AUDIO_DURATION = 'AUDIO_MIN_DURATION_MILLI'
CNN_MODEL_PATH = 'CNN_MODEL_PATH'


@dataclass(frozen=True)
class Settings:
    db_url: str
    jwt_secret_key: str
    jwt_refresh_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    target_sample_rate: int
    audio_min_duration_milli: int
    cnn_model_path: str


def create_settings_instance() -> Settings:
    return Settings(
        db_url=str(os.getenv(DB_URL)),
        jwt_secret_key=str(os.getenv(JWT_SECRET_KEY)),
        jwt_refresh_secret_key=str(os.getenv(JWT_REFRESH_SECRET_KEY)),
        algorithm=str(os.getenv(ALGORITHM)),
        access_token_expire_minutes=int(os.getenv(ACCESS_TOKEN_EXPIRE_MINUTES)),
        refresh_token_expire_days=int(os.getenv(REFRESH_TOKEN_EXPIRE_DAYS)),
        target_sample_rate=int(os.getenv(SAMPLE_RATE)),
        audio_min_duration_milli=int(os.getenv(AUDIO_DURATION)),
        cnn_model_path=os.getenv(CNN_MODEL_PATH)
    )
