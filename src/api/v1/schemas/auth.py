from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from src.api.v1.schemas.base import DetailMixin, ItemsResponse
from src.enums.auth import Role
from src.enums.type import Type


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    picture_url: str
    birthday: datetime
    type: Literal[Type.user] = Type.user


class SUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    picture_url: str
    birthday: datetime
    type: Literal[Type.user] = Type.user


class SMeResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    picture_url: str
    birthday: datetime
    type: Literal[Type.user] = Type.user


class SUsersResponse(ItemsResponse[SUserResponse]):
    pass


class SUpdateUserPictureResponse(BaseModel, DetailMixin):
    detail: str = "User picture updated."


class SUpdateUserRequest(BaseModel):
    name: str | None = None
    username: str | None = None
    description: str | None = None


class SUpdateUserResponse(BaseModel):
    id: int


class SDeleteUserResponse(BaseModel, DetailMixin):
    detail: str = "User deleted."


class SArtistResponse(BaseModel):
    id: int
    user: SUserResponse
    description: str | None = None
    type: Literal[Type.artist] = Type.artist


class SMeAsArtistResponse(BaseModel):
    id: int
    user: SUserResponse
    description: str | None = None
    type: Literal[Type.artist] = Type.artist


class SArtistsResponse(ItemsResponse[SArtistResponse]):
    pass


class SUpdateArtistRequest(BaseModel):
    description: str | None = Field(max_length=255)


class SUpdateArtistResponse(BaseModel):
    id: int


class SDeleteArtistResponse(BaseModel, DetailMixin):
    detail: str = "Artist deleted"


class SProducerResponse(BaseModel):
    id: int
    user: SUserResponse
    description: str | None = None
    type: Literal[Type.producer] = Type.producer


class SMeAsProducerResponse(BaseModel):
    id: int
    user: SUserResponse
    description: str | None = None


class SProducersResponse(ItemsResponse[SProducerResponse]):
    pass


class SUpdateProducerRequest(BaseModel):
    description: str | None = Field(max_length=255)


class SUpdateProducerResponse(BaseModel):
    id: int


class SDeleteProducerResponse(BaseModel, DetailMixin):
    detail: str = "Producer deleted"


class SRegisterUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=25)
    password: str = Field(min_length=5)
    email: EmailStr
    roles: list[Role]
    birthday: date
    tags: list[str] = list()


class SRegisterUserResponse(BaseModel):
    id: int


class SLoginRequest(BaseModel):
    email: EmailStr
    password: str


class SLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: SUserResponse


class SRefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class SSpotifyCallbackResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: SUserResponse
