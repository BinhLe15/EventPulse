"""
Monitored Accounts API endpoints.
Placeholder for future CRUD operations on monitored accounts.
"""
from src.schemas.account import AccountParams
from fastapi import APIRouter

router = APIRouter()


# TODO: Implement CRUD endpoints for monitored accounts
# - POST /accounts - Create new monitored account
# - GET /accounts - List all monitored accounts
# - GET /accounts/{id} - Get specific account
# - PUT /accounts/{id} - Update account
# - DELETE /accounts/{id} - Delete account


@router.get("/")
async def get_users(params: AccountParams):
    pass