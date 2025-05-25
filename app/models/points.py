from sqlmodel import SQLModel, Field, Relationship

from app.models.travels import TravelPublic


class PointBase(SQLModel):
    name: str = Field(index=True)
    type: str = Field(index=True)
    ocatd: str
    code: str

class Point(PointBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    region_id: int = Field(default=None, foreign_key="region.id")
    region: "Region" = Relationship(back_populates="points")

class PointPublic(PointBase):
    id: int

class PointPublicWithRegion(PointPublic):
    region: "RegionPublic"

class PointCreate(PointBase):
    region_id: int = Field(default=None, foreign_key="region.id")

class PointUpdate(PointBase):
    pass

TravelPublic.model_rebuild()
