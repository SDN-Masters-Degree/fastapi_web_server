from fastapi import UploadFile, Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from app.api.schemas import ErrorResponse
from app.api.schemas.audio import AudioResponse
from app.api.depends import valid_audio_file
from app.src.data_extraction import determine_audio_spoof
from app.src.exception import (AudioDurationException,
                               ModelPredictionException)


audio_router = APIRouter(prefix='/audio', tags=['Audio'])


@audio_router.post('/check_spoof')
async def check_spoof(audio_file: UploadFile = Depends(valid_audio_file)) -> JSONResponse:
    try:
        res = await determine_audio_spoof(audio_file.file)
    except (AudioDurationException, ModelPredictionException) as e:
        return JSONResponse(ErrorResponse(detail=str(e)).model_dump(), 404)

    return JSONResponse(AudioResponse(result=res).model_dump())
