"""
API v1 Router aggregator.
Combines all endpoint routers for version 1 of the API.
"""
from fastapi import APIRouter
from src.api.v1.endpoints import accounts, users

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
