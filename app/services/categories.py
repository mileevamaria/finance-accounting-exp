from collections.abc import Sequence
from uuid import UUID

from fastapi import HTTPException, status

from app.models import Category, CategoryGroup, Company
from app.repositories import (
    CategoryGroupRepository,
    CategoryRepository,
    CompanyRepository,
)
from app.schemas.categories import (
    CategoryCreate,
    CategoryGroupCreate,
    CategoryGroupUpdate,
    CategoryUpdate,
)


class CategoryGroupService:
    def __init__(
        self,
        group_repo: CategoryGroupRepository,
        company_repo: CompanyRepository,
    ):
        self.group_repo = group_repo
        self.company_repo = company_repo

    async def _get_company_or_404(
        self,
        company_id: UUID,
        owner_id: UUID,
    ) -> Company:
        company = await self.company_repo.get_by_id(company_id)

        if company is None or company.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Company not found',
            )

        return company

    async def create(
        self,
        company_id: UUID,
        owner_id: UUID,
        data: CategoryGroupCreate,
    ) -> CategoryGroup:
        await self._get_company_or_404(company_id, owner_id)

        group = CategoryGroup(
            company_id=company_id,
            **data.model_dump(),
        )

        return await self.group_repo.create(group)

    async def get_company_groups(
        self,
        company_id: UUID,
        owner_id: UUID,
    ) -> Sequence[CategoryGroup]:
        await self._get_company_or_404(company_id, owner_id)

        return await self.group_repo.get_by_company(company_id)

    async def get_group(
        self,
        group_id: UUID,
        company_id: UUID,
        owner_id: UUID,
    ) -> CategoryGroup:
        await self._get_company_or_404(company_id, owner_id)

        group = await self.group_repo.get_by_id(group_id)

        if group is None or group.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category group not found',
            )

        return group

    async def update(
        self,
        group_id: UUID,
        company_id: UUID,
        owner_id: UUID,
        data: CategoryGroupUpdate,
    ) -> CategoryGroup:
        group = await self.get_group(
            group_id=group_id,
            company_id=company_id,
            owner_id=owner_id,
        )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(group, field, value)

        return await self.group_repo.update(group)


class CategoryService:
    def __init__(
        self,
        category_repo: CategoryRepository,
        group_service: CategoryGroupService,
    ):
        self.category_repo = category_repo
        self.group_service = group_service

    async def create(
        self,
        company_id: UUID,
        owner_id: UUID,
        data: CategoryCreate,
    ) -> Category:
        group = await self.group_service.get_group(
            group_id=data.group_id,
            company_id=company_id,
            owner_id=owner_id,
        )

        category = Category(
            company_id=company_id,
            group_id=group.id,
            name=data.name,
            icon_color=data.icon_color,
        )

        return await self.category_repo.create(category)

    async def get_company_categories(
        self,
        company_id: UUID,
        owner_id: UUID,
    ) -> Sequence[Category]:
        await self.group_service._get_company_or_404(
            company_id,
            owner_id,
        )

        return await self.category_repo.get_by_company(company_id)

    async def get_category(
        self,
        category_id: UUID,
        company_id: UUID,
        owner_id: UUID,
    ) -> Category:
        await self.group_service._get_company_or_404(
            company_id,
            owner_id,
        )

        category = await self.category_repo.get_by_id(category_id)

        if category is None or category.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found',
            )

        return category

    async def update(
        self,
        category_id: UUID,
        company_id: UUID,
        owner_id: UUID,
        data: CategoryUpdate,
    ) -> Category:
        category = await self.get_category(
            category_id=category_id,
            company_id=company_id,
            owner_id=owner_id,
        )

        if data.group_id is not None:
            group = await self.group_service.get_group(
                group_id=data.group_id,
                company_id=company_id,
                owner_id=owner_id,
            )
            category.group_id = group.id

        update_data = data.model_dump(
            exclude_unset=True,
            exclude={'group_id'},
        )

        for field, value in update_data.items():
            setattr(category, field, value)

        return await self.category_repo.update(category)
