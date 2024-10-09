from fastapi import UploadFile, Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from app.api.depends import valid_audio_file
from app.src.data_extraction import determine_audio_auth

audio_router = APIRouter(prefix='/audio', tags=['Audio'])


@audio_router.post('/recognize')
async def recognize(audio_file: UploadFile = Depends(valid_audio_file)) -> JSONResponse:
    res = await determine_audio_auth(audio_file.file)

    return JSONResponse({'result': res.value})
