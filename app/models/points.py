from sqlmodel import SQLModel, Field, Relationship

class Point(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: str = Field(index=True)
    ocatd: str
    code: str
    region_id: int = Field(default=None, foreign_key="region.id")
    region: "Region" = Relationship(back_populates="points")
