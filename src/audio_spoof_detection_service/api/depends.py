from fastapi import UploadFile
from fastapi.exceptions import HTTPException


async def valid_audio_file(file: UploadFile) -> UploadFile:
    allowed_audio_extensions = ('.mp3', '.wav', '.ogg')
    file_name: str = file.filename

    if not file_name.endswith(allowed_audio_extensions):
        raise HTTPException(detail=f'{file_name} is not allowed extension '
                                   f'(use {allowed_audio_extensions})',
                            status_code=404)

    return file
