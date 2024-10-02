from datetime import datetime
from typing import Literal

from src.dtos.database.base import BaseResponseDTO, BaseRequestDTO, BaseDTO
from src.enums.type import Type


class Album(BaseDTO):
    id: int
    title: str
    picture_url: str | None = None
    description: str
    co_prod: str | None = None
    type: Literal[Type.album] = Type.album
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_available: bool


class CreateAlbumRequestDTO(BaseRequestDTO):
    name: str
    picture_url: str
    description: str
    prod_by: str
    co_prod: str | None = None
    type: Literal[Type.album] = Type.album
    user_id: int


class UpdateAlbumRequestDTO(BaseRequestDTO):
    id: int
    name: str | None = None
    picture_url: str | None = None
    description: str | None = None
    co_prod: str | None = None
    type: Literal[Type.album] = Type.album
    user_id: int


class AlbumResponseDTO(BaseResponseDTO):
    id: int
    name: str
    picture_url: str
    description: str
    co_prod: str
    type: Literal[Type.album] = Type.album
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_available: bool


class AlbumsResponseDTO(BaseResponseDTO):
    albums: list[AlbumResponseDTO]
