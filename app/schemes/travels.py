from datetime import datetime
import enum
from sqlmodel import SQLModel, Field

class StatusChoices(enum.Enum):
    PlANNED = 'Planned'
    COMPLETED = 'Completed'
    CANCELED = 'Cancelled'

class StatusPassengerChoices(str, enum.Enum):
    REQUESTED = "Requested"
    ACCEPTED = "Accepted"

class TravelBase(SQLModel):
    date: datetime = Field(description="Дата поездки")
    status: StatusChoices = StatusChoices.PlANNED
    number_of_available_seats: int = Field(default=0)

class TravelUserPublic(SQLModel):
    user_id: int
    status: StatusPassengerChoices

class TravelUserCreate(SQLModel):
    user_id: int = None

class TravelPublic(TravelBase):
    id: int
    starting_point: "PointPublic" = None
    end_point: "PointPublic" = None
    driver: "UserPublic" = None

class TravelCreate(TravelBase):
    starting_point_id: int = Field(default=None, foreign_key="point.id")
    end_point_id: int = Field(default=None, foreign_key="point.id")
    driver_id: int = Field(default=None, foreign_key="user.id")

class TravelUpdate(TravelBase):
    pass

