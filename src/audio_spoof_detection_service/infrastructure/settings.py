import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()

SAMPLE_RATE = 'TARGET_SAMPLE_RATE'
AUDIO_DURATION = 'AUDIO_MIN_DURATION_MILLI'
CNN_MODEL_PATH = 'CNN_MODEL_PATH'


@dataclass(frozen=True)
class Settings:
    target_sample_rate: int
    audio_min_duration_milli: int
    cnn_model_path: str


def create_settings_instance() -> Settings:
    return Settings(
        target_sample_rate=int(os.getenv(SAMPLE_RATE)),
        audio_min_duration_milli=int(os.getenv(AUDIO_DURATION)),
        cnn_model_path=os.getenv(CNN_MODEL_PATH)
    )
