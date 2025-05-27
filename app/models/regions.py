from sqlmodel import SQLModel, Field, Relationship

class Region(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: str = Field(index=True, description="Тип региона")
    points: list["Point"] = Relationship(back_populates="region")
    users: list["User"] = Relationship(back_populates="region")
