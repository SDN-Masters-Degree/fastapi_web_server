from fastapi.responses import JSONResponse
from fastapi.requests import Request

from audio_spoof_detection_service.api.schemas.error import ErrorResponse


async def audio_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    response = ErrorResponse(detail=str(exc))
    return JSONResponse(response.model_dump(), 409)


async def neural_model_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    response = ErrorResponse(detail=str(exc))
    return JSONResponse(response.model_dump(), 500)
