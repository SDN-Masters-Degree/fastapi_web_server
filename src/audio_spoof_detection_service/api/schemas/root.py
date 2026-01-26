from pydantic import BaseModel


class RootResponse(BaseModel):
    message: str


class CheckHealthResponse(BaseModel):
    status: str
