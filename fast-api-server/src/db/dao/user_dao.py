from typing import Optional
from sqlalchemy import select, func, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.db.models.users_model import UserModel
from src.schemas import Pagination

class UserDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(self, user_id: int) -> UserModel:
        try:
            result = await self.db_session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            user_instance = result.scalar_one_or_none()
            return user_instance
        except SQLAlchemyError as e:
            print(f"Error fetching User by ID: {e}")
            return None
        
    async def create_user(self, user_data: dict) -> UserModel:
        try:
            new_user = UserModel(**user_data)
            self.db_session.add(new_user)
            await self.db_session.commit()
            await self.db_session.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            print(f"Error creating User: {e}")
            return None

    async def get_users(self, limit: int, offset: int, sort_by: str, sort_order: str) -> Pagination:
        try:
            query = select(UserModel)

            if sort_order.lower() == "asc":
                query = query.order_by(asc(getattr(UserModel, sort_by)))
            else:
                query = query.order_by(desc(getattr(UserModel, sort_by)))

            total_result = await self.db_session.execute(
                select(func.count()).select_from(UserModel)
            )
            total_count = total_result.scalar_one()

            result = await self.db_session.execute(
                query.limit(limit).offset(offset)
            )
            users = list(result.scalars().all())

            return Pagination(
                cursor=offset,
                count=len(users),
                remaining=max(0, total_count - (len(users) + offset)),
                results=users,
            )
        except SQLAlchemyError as e:
            print(f"Error fetching Users: {e}")
            return Pagination(
                cursor=offset,
                count=0,
                remaining=0,
                results=[],
            )