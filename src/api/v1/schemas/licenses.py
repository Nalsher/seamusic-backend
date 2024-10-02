from datetime import datetime

from pydantic import BaseModel

from src.api.v1.schemas.base import DetailMixin, ItemsResponse


class SLicenseResponse(BaseModel):
    id: int
    title: str
    picture_url: str | None = None
    description: str | None = None
    file_path: str
    co_prod: str | None = None
    prod_by: str | None = None
    playlist_id: int | None = None
    user_id: int
    beat_pack_id: int | None = None
    price: str
    created_at: datetime
    updated_at: datetime


class SLicensesResponse(ItemsResponse[SLicenseResponse]):
    pass


class SMyLicensesResponse(ItemsResponse[SLicenseResponse]):
    pass


class SCreateLicenseRequest(BaseModel):
    title: str
    description: str
    price: str


class SCreateLicenseResponse(BaseModel):
    id: int


class SEditLicenseRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: str | None = None


class SEditLicensesResponse(BaseModel):
    id: int


class SLicensesDeleteResponse(BaseModel, DetailMixin):
    detail: str = "License deleted"
