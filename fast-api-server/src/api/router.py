from fastapi import Security, APIRouter
from fast_api_auth0 import Auth0
from src.settings import settings
from src.api import example

api_router = APIRouter()
auth = Auth0()
dependencies = []

if not settings.debug:
    dependencies.append(Security(auth.verify))

api_router.include_router(
    example.router,
    prefix="/examples",
    tags=["example"],
    dependencies=dependencies,
)
