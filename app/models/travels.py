# travels.py
from datetime import datetime
import enum
from sqlmodel import SQLModel, Field, Relationship


class StatusChoices(enum.Enum):
    PlANNED = 'Planned'
    COMPLETED = 'Completed'
    CANCELED = 'Cancelled'

class TravelBase(SQLModel):
    date: datetime = Field(description="Дата поездки")
    status: StatusChoices = StatusChoices.PlANNED
    number_of_available_seats: int = Field(default=0)

class TravelUserLink(SQLModel, table=True):
    travel_id: int | None = Field(default=None, foreign_key="travel.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)

class Travel(TravelBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    starting_point_id: int = Field(default=None, foreign_key="point.id")
    end_point_id: int = Field(default=None, foreign_key="point.id")
    driver_id: int = Field(default=None, foreign_key="user.id")

    starting_point: "Point" = Relationship(sa_relationship_kwargs={"foreign_keys": "Travel.starting_point_id"})
    end_point: "Point" = Relationship(sa_relationship_kwargs={"foreign_keys": "Travel.end_point_id"})
    driver: "User" = Relationship()
    passengers: list["User"] = Relationship(back_populates="travels", link_model=TravelUserLink)

    # @field_validator("date")
    # @classmethod
    # def validate_date(cls, values: datetime):
    #     if values and values >= datetime.now().date():
    #         raise ValueError("Дата поездки должна быть позже текущей даты")
    #     return values


class TravelPublic(TravelBase):
    id: int
    starting_point: "PointPublic" = None
    end_point: "PointPublic" = None
    driver_id: int = None

class TravelCreate(TravelBase):
    starting_point_id: int = Field(default=None, foreign_key="point.id")
    end_point_id: int = Field(default=None, foreign_key="point.id")
    driver_id: int = Field(default=None, foreign_key="user.id")

class TravelUpdate(TravelBase):
    pass

