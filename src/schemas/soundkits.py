from datetime import datetime

from pydantic import BaseModel

from src.schemas.base import DetailMixin


class Soundkit(BaseModel):
    id: int
    title: str
    picture: str | None = None
    description: str | None = None
    file_path: str
    co_prod: str | None = None
    prod_by: str | None = None
    playlist_id: int | None = None
    user_id: int
    beatpack_id: int | None = None


class SSoundkitResponse(BaseModel):
    id: int
    name: str
    co_prod: str
    prod_by: str
    description: str
    picture_url: str
    file_url: str
    user_id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime


class SAllSoundkitsResponse(BaseModel):
    total: int
    page: int
    has_next: bool
    has_previous: bool
    size: int
    items: list[SSoundkitResponse]


class SMySoundkitsResponse(BaseModel):
    total: int
    page: int
    has_next: bool
    has_previous: bool
    size: int
    items: list[SSoundkitResponse]


class SCreateSoundkitRequest(BaseModel):
    title: str
    picture: str | None = None
    description: str | None = None
    file_path: str
    co_prod: str | None = None
    prod_by: str | None = None
    playlist_id: int | None = None
    user_id: int
    beatpack_id: int | None = None


class SCreateSoundkitResponse(BaseModel):
    id: int


class SUpdateSoundkitRequest(BaseModel):
    title: str | None = None
    picture: str | None = None
    description: str | None = None
    co_prod: str | None = None
    prod_by: str | None = None


class SUpdateSoundkitResponse(BaseModel):
    id: int


class SSoundkitDeleteResponse(BaseModel, DetailMixin):
    detail: str = "Soundkit deleted"
