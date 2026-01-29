"""
Users API endpoints.
Placeholder for future user management operations.
"""
from src.services.user import user_service
from src.schemas.user import UserParams
from fastapi import APIRouter, Depends

router = APIRouter()


# TODO: Implement user management endpoints if needed
# - POST /users - Create new user
# - GET /users - List all users
# - GET /users/{id} - Get specific user
# - PUT /users/{id} - Update user
# - DELETE /users/{id} - Delete user


@router.get("/")
async def get_users(params: UserParams = Depends(UserParams)):
    return await user_service.get_all_users(params)