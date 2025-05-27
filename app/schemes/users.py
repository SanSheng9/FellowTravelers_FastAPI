from typing import Optional

from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username: str = Field(index=True)
    chat_id: int = Field(index=True)
    average_rating: Optional[float] = None

class UserPublic(UserBase):
    id: int

class UserPublicWithRegion(UserPublic):
    region: "RegionPublic" = None

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    region_id: int
