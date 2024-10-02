from fastapi import UploadFile, File, APIRouter, Depends, status

from src.api.v1.schemas.auth import User
from src.api.v1.schemas.base import Page, get_items_response
from src.api.v1.schemas.beats import (
    SBeatReleaseRequest,
    SBeatReleaseResponse,
    SBeatResponse,
    SBeatsResponse,
    SCreateBeatResponse,
    SDeleteBeatResponse,
    SMyBeatsResponse,
    SUpdateBeatPictureResponse,
)
from src.api.v1.schemas.beats import SBeatUpdateRequest, SBeatUpdateResponse
from src.api.v1.utils.auth import get_current_user
from src.services.beats import BeatsService, get_beats_service
from src.utils.files import unique_filename, get_file_stream

beats = APIRouter(prefix="/beats", tags=["Beats"])


@beats.get(
    path="/my",
    summary="Beats by current user",
    status_code=status.HTTP_200_OK,
    response_model=SMyBeatsResponse,
    responses={status.HTTP_200_OK: {"model": SMyBeatsResponse}},
)
async def get_my_beats(
    page: Page = Depends(Page),
    user: User = Depends(get_current_user),
    service: BeatsService = Depends(get_beats_service),
) -> SMyBeatsResponse:

    response = await service.get_user_beats(user_id=user.id, start=page.start, size=page.size)

    items = list(map(
        lambda beat: SBeatResponse(
            id=beat.id,
            title=beat.title,
            description=beat.description,
            picture_url=beat.picture_url,
            file_url=beat.file_url,
            co_prod=beat.co_prod,
            prod_by=beat.co_prod,
            user_id=beat.user_id,
            is_available=beat.is_available,
            created_at=beat.created_at,
            updated_at=beat.updated_at,
        ),
        response.beats
    ))

    total = await service.get_user_beats_count(user_id=user.id)

    return get_items_response(
        start=page.start,
        size=page.size,
        total=total,
        items=items,
        response_model=SMyBeatsResponse,
    )


@beats.get(
    path="/",
    summary="Get all beats",
    response_model=SBeatsResponse,
    responses={status.HTTP_200_OK: {"model": SBeatsResponse}},
)
async def get_all_beats(
    page: Page = Depends(Page),
    service: BeatsService = Depends(get_beats_service),
) -> SBeatsResponse:

    response = await service.get_all_beats(start=page.start, size=page.size)

    items = list(map(
        lambda beat: SBeatResponse(
            id=beat.id,
            title=beat.title,
            description=beat.description,
            picture_url=beat.picture_url,
            file_url=beat.file_url,
            co_prod=beat.co_prod,
            prod_by=beat.co_prod,
            user_id=beat.user_id,
            is_available=beat.is_available,
            created_at=beat.created_at,
            updated_at=beat.updated_at,
        ),
        response.beats
    ))

    total = await service.get_all_beats_count()

    return get_items_response(
        start=page.start,
        size=page.size,
        total=total,
        items=items,
        response_model=SBeatsResponse,
    )


@beats.get(
    path="/{beat_id}",
    summary="Get one beat by id",
    response_model=SBeatResponse,
    responses={status.HTTP_200_OK: {"model": SBeatResponse}},
)
async def get_beat_by_id(
    beat_id: int,
    service: BeatsService = Depends(get_beats_service),
) -> SBeatResponse:

    beat = await service.get_beat_by_id(beat_id=beat_id)
    return SBeatResponse(
        id=beat.id,
        title=beat.title,
        description=beat.description,
        picture_url=beat.picture_url,
        file_url=beat.file_url,
        co_prod=beat.co_prod,
        prod_by=beat.prod_by,
        user_id=beat.user_id,
        is_available=beat.is_available,
        created_at=beat.created_at,
        updated_at=beat.updated_at
    )


@beats.post(
    path="/",
    summary="Init a beat with file",
    response_model=SCreateBeatResponse,
    responses={status.HTTP_200_OK: {"model": SCreateBeatResponse}},
)
async def add_beat(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    service: BeatsService = Depends(get_beats_service)
) -> SCreateBeatResponse:

    file_info = unique_filename(file)
    file_stream = await get_file_stream(file)

    beat_id = await service.add_beat(
        file_stream=file_stream,
        user_id=user.id,
        prod_by=user.username,
        co_prod=None,
        file_info=file_info,
    )

    return SCreateBeatResponse(id=beat_id)


@beats.put(
    path="/{beat_id}/picture",
    summary="Update a picture for one beat by id",
    response_model=SUpdateBeatPictureResponse,
    responses={status.HTTP_200_OK: {"model": SUpdateBeatPictureResponse}},
)
async def update_beat_picture(
    beat_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    service: BeatsService = Depends(get_beats_service)
) -> SUpdateBeatPictureResponse:

    beat_id = await service.update_pic_beats(
        beat_id=beat_id,
        user_id=user.id,
        file_info=unique_filename(file),
        file_stream=await get_file_stream(file)
    )

    return SUpdateBeatPictureResponse(id=beat_id)


@beats.post(
    path="/{beat_id}/release",
    summary="Release one beat by id",
    response_model=SBeatReleaseResponse,
    responses={status.HTTP_200_OK: {"model": SBeatReleaseResponse}},
)
async def release_beat(
    beat_id: int,
    data: SBeatReleaseRequest,
    user: User = Depends(get_current_user),
    service: BeatsService = Depends(get_beats_service)
) -> SBeatReleaseResponse:

    beat_id = await service.release_beat(
        beat_id=beat_id,
        user_id=user.id,
        title=data.title,
        description=data.description,
        co_prod=data.co_prod,
        prod_by=data.co_prod
    )

    return SBeatReleaseResponse(id=beat_id)


@beats.put(
    path="/{beat_id}",
    summary="Edit beat by id",
    response_model=SBeatUpdateResponse,
    responses={status.HTTP_200_OK: {"model": SBeatUpdateResponse}},
)
async def update_beat(
    beat_id: int,
    data: SBeatUpdateRequest,
    user: User = Depends(get_current_user),
    service: BeatsService = Depends(get_beats_service)
) -> SBeatUpdateResponse:

    beat_id = await service.update_beat(
        beat_id=beat_id,
        user_id=user.id,
        title=data.title,
        description=data.description,
        co_prod=data.co_prod,
        prod_by=data.prod_by
    )

    return SBeatUpdateResponse(id=beat_id)


@beats.delete(
    path="/{beat_id}",
    summary="delete beat by id",
    response_model=SDeleteBeatResponse,
    responses={status.HTTP_200_OK: {"model": SDeleteBeatResponse}},
)
async def delete_beat(
    beat_id: int,
    user: User = Depends(get_current_user),
    service: BeatsService = Depends(get_beats_service)
) -> SDeleteBeatResponse:

    await service.delete_beat(beat_id=beat_id, user_id=user.id)

    return SDeleteBeatResponse()
