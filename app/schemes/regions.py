from sqlmodel import SQLModel, Field


class RegionBase(SQLModel):
    name: str = Field(index=True)
    type: str = Field(index=True, description="Тип региона")

class RegionPublic(RegionBase):
    id: int

class RegionPublicWithPoints(RegionPublic):
    points: list["Point"]

class RegionCreate(RegionBase):
    pass

class RegionUpdate(RegionBase):
    pass


