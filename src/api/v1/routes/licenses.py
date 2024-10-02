from fastapi import APIRouter, Depends, status

from src.api.v1.schemas.base import Page, get_items_response
from src.api.v1.schemas.licenses import (
    SMyLicensesResponse,
    SLicensesResponse,
    SLicenseResponse,
    SCreateLicenseResponse,
    SCreateLicenseRequest,
    SEditLicensesResponse,
    SLicensesDeleteResponse,
    SEditLicenseRequest,
)
from src.api.v1.utils.auth import get_current_user
from src.models.auth import User
from src.services.licenses import LicensesService, get_licenses_service

licenses = APIRouter(prefix="/licenses", tags=["Licenses"])


@licenses.post(
    path="/my",
    summary="Packs by current user",
    response_model=SMyLicensesResponse,
    responses={status.HTTP_200_OK: {"model": SMyLicensesResponse}},
)
async def get_my_licenses(
    page: Page = Depends(Page),
    user: User = Depends(get_current_user),
    service: LicensesService = Depends(get_licenses_service),
) -> SMyLicensesResponse:

    response = await service.get_user_licenses(user_id=user.id, start=page.start, size=page.size)

    items = list(map(
        lambda license_: SLicenseResponse(
            id=license_.id,
            title=license_.title,
            picture_url=license_.picture_url,
            description=license_.description,
            file_path=license_.file_path,
            co_prod=license_.co_prod,
            prod_by=license_.prod_by,
            playlist_id=license_.playlist_id,
            user_id=license_.user_id,
            beat_pack_id=license_.beat_pack_id,
            price=license_.price,
            created_at=license_.created_at,
            updated_at=license_.updated_at,
        ),
        response.licenses
    ))

    total = await service.get_user_licenses_count(user_id=user.id)

    return get_items_response(
        start=page.start,
        size=page.size,
        total=total,
        items=items,
        response_model=SMyLicensesResponse,
    )


@licenses.get(
    path="/",
    summary="Get all licenses",
    response_model=SLicensesResponse,
    responses={status.HTTP_200_OK: {"model": SLicensesResponse}},
)
async def get_all_licenses(
    page: Page = Depends(Page),
    service: LicensesService = Depends(get_licenses_service),
) -> SLicensesResponse:

    response = await service.get_all_licenses(start=page.start, size=page.size)

    items = list(map(
        lambda license_: SLicenseResponse(
            id=license_.id,
            title=license_.title,
            picture_url=license_.picture_url,
            description=license_.description,
            file_path=license_.file_path,
            co_prod=license_.co_prod,
            prod_by=license_.prod_by,
            playlist_id=license_.playlist_id,
            user_id=license_.user_id,
            beat_pack_id=license_.beat_pack_id,
            price=license_.price,
            created_at=license_.created_at,
            updated_at=license_.updated_at,
        ),
        response.licenses
    ))

    total = await service.get_licenses_count()

    return get_items_response(
        start=page.start,
        size=page.size,
        total=total,
        items=items,
        response_model=SMyLicensesResponse,
    )


@licenses.get(
    path="/{license_id}",
    summary="Get license by id",
    response_model=SLicenseResponse,
    responses={status.HTTP_200_OK: {"model": SLicenseResponse}},
)
async def get_one(
    license_id: int,
    service: LicensesService = Depends(get_licenses_service),
) -> SLicenseResponse:

    license_ = await service.get_one(license_id=license_id)

    return SLicenseResponse(
        id=license_.id,
        title=license_.title,
        picture_url=license_.picture_url,
        description=license_.description,
        file_path=license_.file_path,
        co_prod=license_.co_prod,
        prod_by=license_.prod_by,
        playlist_id=license_.playlist_id,
        user_id=license_.user_id,
        beat_pack_id=license_.beat_pack_id,
        price=license_.price,
        created_at=license_.created_at,
        updated_at=license_.updated_at,
    )


@licenses.post(
    path="/new",
    summary="Add a file for new beat",
    response_model=SCreateLicenseResponse,
    responses={status.HTTP_200_OK: {"model": SCreateLicenseResponse}},
)
async def add_license(
    data: SCreateLicenseRequest,
    user: User = Depends(get_current_user),
    service: LicensesService = Depends(get_licenses_service),
) -> SCreateLicenseResponse:

    license_id = await service.add_license(
        title=data.title,
        price=data.price,
        user_id=user.id,
        description=data.description,
    )

    return SCreateLicenseResponse(id=license_id)


@licenses.put(
    path="/{license_id}/update",
    summary="Edit license by id",
    response_model=SEditLicensesResponse,
    responses={status.HTTP_200_OK: {"model": SEditLicensesResponse}},
)
async def update_license(
    license_id: int,
    data: SEditLicenseRequest,
    user: User = Depends(get_current_user),
    service: LicensesService = Depends(get_licenses_service),
) -> SEditLicensesResponse:

    license_id = await service.update_license(
        license_id=license_id,
        user_id=user.id,
        title=data.title,
        description=data.description,
        price=data.price,
    )

    return SEditLicensesResponse(id=license_id)


@licenses.delete(
    path="/{license_id}/delete",
    summary="Create new licenses",
    response_model=SLicensesDeleteResponse,
    responses={status.HTTP_200_OK: {"model": SLicensesDeleteResponse}},
)
async def delete_licenses(
    license_id: int,
    user: User = Depends(get_current_user),
    service: LicensesService = Depends(get_licenses_service)
) -> SLicensesDeleteResponse:

    await service.delete_license(license_id=license_id, user_id=user.id)
    return SLicensesDeleteResponse()
