from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.users_model import UserModel
from src.db.dao.user_dao import UserDAO
from src.schemas import Pagination
from src.api.users.schema import UserSchema, UserPayload

class Users:
    def __init__(self, db_session: AsyncSession):
        self.user_dao = UserDAO(db_session)

    async def get_user_by_id(self, user_id: int) -> UserSchema:
        result = await self.user_dao.get_user_by_id(user_id)
        return UserSchema.model_validate(result)
    
    async def create_user(self, user_data: UserPayload) -> UserSchema:
        new_user = await self.user_dao.create_user(user_data.model_dump())
        return UserSchema.model_validate(new_user)
    
    async def get_users(self, limit: int, offset: int, sort_by: str, sort_order: str) -> Pagination[UserSchema]:
        users_page = await self.user_dao.get_users(
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        # Convert SQLAlchemy models to Pydantic schemas
        user_schemas = [UserSchema.model_validate(user) for user in users_page.results]
        return Pagination(
            cursor=users_page.cursor,
            count=users_page.count,
            remaining=users_page.remaining,
            results=user_schemas
        )