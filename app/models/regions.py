from sqlmodel import SQLModel, Field, Relationship

from app.models.points import PointPublicWithRegion
from app.models.users import UserPublicWithRegion


class RegionBase(SQLModel):
    name: str = Field(index=True)
    type: str = Field(index=True, description="Тип региона")


class Region(RegionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    points: list["Point"] = Relationship(back_populates="region")
    users: list["User"] = Relationship(back_populates="region")

class RegionPublic(RegionBase):
    id: int

class RegionPublicWithPoints(RegionPublic):
    points: list["Point"]

class RegionCreate(RegionBase):
    pass

class RegionUpdate(RegionBase):
    pass

PointPublicWithRegion.model_rebuild()
UserPublicWithRegion.model_rebuild()
