from pydantic import BaseModel

from app.src.data_extraction import AudioResult


class AudioResponse(BaseModel):
    result: AudioResult
