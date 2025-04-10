from fastapi import APIRouter
from src.api import (example, fixture)

api_router = APIRouter()

api_router.include_router(
    example.router,
    prefix="/examples",
    tags=["example"],
)
api_router.include_router(
    fixture.router,
    prefix="/fixtures",
    tags=["fixture"],
)
