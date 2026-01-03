from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fast_api_db import get_db_session
from src.api.users.service import Users
from src.api.users.schema import UserSchema, UserPayload
from src.schemas import Pagination

router = APIRouter()

@router.get("/", response_model=Pagination[UserSchema])
async def get_users(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "id",
    sort_order: str = "asc",
):
    users_service = Users(db_session)
    users_page = await users_service.get_users(
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return users_page

@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    users_service = Users(db_session)
    user = await users_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserSchema)
async def create_user(user: UserPayload, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    users_service = Users(db_session)
    new_user = await users_service.create_user(user)
    return new_user