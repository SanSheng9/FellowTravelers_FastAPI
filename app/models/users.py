import enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from app.models.travels import TravelUserLink


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    chat_id: int = Field(index=True)
    average_rating: Optional[float] = None
    region_id: int = Field(default=None, foreign_key="region.id")
    region: "Region" = Relationship(back_populates='users')

    travels: list["Travel"] = Relationship(
        back_populates="passengers",
        link_model=TravelUserLink)