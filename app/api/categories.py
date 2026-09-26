from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import (
    CategoryGroupServiceDep,
    CategoryServiceDep,
    CurrentUserDep,
)
from app.schemas.categories import (
    CategoryCreate,
    CategoryGroupCreate,
    CategoryGroupResponse,
    CategoryGroupUpdate,
    CategoryResponse,
    CategoryUpdate,
)

router = APIRouter(
    prefix='/companies/{company_id}',
    tags=['Categories'],
)


@router.post('/category-groups', response_model=CategoryGroupResponse)
async def create_group(
    company_id: UUID,
    data: CategoryGroupCreate,
    current_user: CurrentUserDep,
    service: CategoryGroupServiceDep,
):
    group = await service.create(
        company_id=company_id,
        owner_id=current_user.id,
        data=data,
    )

    return CategoryGroupResponse.model_validate(group)


@router.get('/category-groups', response_model=list[CategoryGroupResponse])
async def get_groups(
    company_id: UUID,
    current_user: CurrentUserDep,
    service: CategoryGroupServiceDep,
):
    groups = await service.get_all(
        company_id=company_id,
        owner_id=current_user.id,
    )

    return [
        CategoryGroupResponse.model_validate(group)
        for group in groups
    ]


@router.get(
    '/category-groups/{group_id}',
    response_model=CategoryGroupResponse,
)
async def get_group(
    company_id: UUID,
    group_id: UUID,
    current_user: CurrentUserDep,
    service: CategoryGroupServiceDep,
):
    group = await service.get_group(
        group_id=group_id,
        company_id=company_id,
        owner_id=current_user.id,
    )

    return CategoryGroupResponse.model_validate(group)


@router.patch(
    '/category-groups/{group_id}',
    response_model=CategoryGroupResponse,
)
async def update_group(
    company_id: UUID,
    group_id: UUID,
    data: CategoryGroupUpdate,
    current_user: CurrentUserDep,
    service: CategoryGroupServiceDep,
):
    group = await service.update(
        group_id=group_id,
        company_id=company_id,
        owner_id=current_user.id,
        data=data,
    )

    return CategoryGroupResponse.model_validate(group)


@router.delete(
    '/category-groups/{group_id}', 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
    group_id: UUID,
    service: CategoryGroupServiceDep,
):
    await service.delete(group_id)


@router.post('/categories', response_model=CategoryResponse)
async def create_category(
    company_id: UUID,
    data: CategoryCreate,
    current_user: CurrentUserDep,
    service: CategoryServiceDep,
):
    category = await service.create(
        company_id=company_id,
        owner_id=current_user.id,
        data=data,
    )

    return CategoryResponse.model_validate(category)


@router.get('/categories', response_model=list[CategoryResponse])
async def get_categories(
    company_id: UUID,
    current_user: CurrentUserDep,
    service: CategoryServiceDep,
):
    categories = await service.get_all(
        company_id=company_id,
        owner_id=current_user.id,
    )

    return [
        CategoryResponse.model_validate(category)
        for category in categories
    ]


@router.get(
    '/categories/{category_id}',
    response_model=CategoryResponse,
)
async def get(
    company_id: UUID,
    category_id: UUID,
    current_user: CurrentUserDep,
    service: CategoryServiceDep,
):
    category = await service.get(
        category_id=category_id,
        company_id=company_id,
        owner_id=current_user.id,
    )

    return CategoryResponse.model_validate(category)


@router.patch(
    '/categories/{category_id}',
    response_model=CategoryResponse,
)
async def update_category(
    company_id: UUID,
    category_id: UUID,
    data: CategoryUpdate,
    current_user: CurrentUserDep,
    service: CategoryServiceDep,
):
    category = await service.update(
        category_id=category_id,
        company_id=company_id,
        owner_id=current_user.id,
        data=data,
    )

    return CategoryResponse.model_validate(category)


@router.delete(
    '/categories/{category_id}', 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: UUID,
    service: CategoryGroupServiceDep,
):
    await service.delete(category_id)
