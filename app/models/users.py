from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from app.models.travels import TravelUserLink, TravelPublic


class UserBase(SQLModel):
    username: str = Field(index=True)
    chat_id: int = Field(index=True)
    average_rating: Optional[float] = None

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    region_id: int = Field(default=None, foreign_key="region.id")
    region: "Region" = Relationship(back_populates='users')

    travels: list["Travel"] = Relationship(
        back_populates="passengers",
        link_model=TravelUserLink)


class UserPublic(UserBase):
    id: int

class UserPublicWithRegion(UserPublic):
    region: "Region" = None

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    region_id: int


TravelPublic.model_rebuild()
