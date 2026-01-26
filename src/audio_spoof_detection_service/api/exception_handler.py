from fastapi.responses import JSONResponse
from fastapi.requests import Request

from audio_spoof_detection_service.api.schemas.error import ErrorResponse


async def domain_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    response = ErrorResponse(detail=str(exc))
    return JSONResponse(response.model_dump(mode='json'), 409)
