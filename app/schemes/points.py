from sqlmodel import SQLModel, Field, Relationship

class PointBase(SQLModel):
    name: str = Field(index=True)
    type: str = Field(index=True)
    ocatd: str
    code: str

class PointPublic(PointBase):
    id: int

class PointPublicWithRegion(PointPublic):
    region: "RegionPublic"

class PointCreate(PointBase):
    region_id: int = Field(default=None, foreign_key="region.id")

class PointUpdate(PointBase):
    pass

