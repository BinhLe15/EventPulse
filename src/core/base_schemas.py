from pydantic import BaseModel, Field


class BasePagination(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(
        default=20, ge=1, le=2000, description="Number of items per page (max 2000)"
    )