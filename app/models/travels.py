from datetime import datetime, timedelta
import enum

from pydantic import field_validator, model_validator
from sqlmodel import SQLModel, Field, Relationship

class StatusPassengerChoices(str, enum.Enum):
    REQUESTED = "Requested"
    ACCEPTED = "Accepted"

class TravelUserLink(SQLModel, table=True):
    travel_id: int | None = Field(default=None, foreign_key="travel.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    status: StatusPassengerChoices = Field(default=StatusPassengerChoices.REQUESTED)

class StatusChoices(str, enum.Enum):
    PLANNED = 'Planned'
    COMPLETED = 'Completed'
    CANCELED = 'Cancelled'

class Travel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: datetime = Field(description="Дата поездки")
    status: StatusChoices = StatusChoices.PLANNED
    number_of_available_seats: int = Field(nullable=False)
    current_number_of_available_seats: int = Field(nullable=False)
    starting_point_id: int = Field(default=None, foreign_key="point.id")
    end_point_id: int = Field(default=None, foreign_key="point.id")
    driver_id: int = Field(default=None, foreign_key="user.id")

    starting_point: "Point" = Relationship(sa_relationship_kwargs={"foreign_keys": "Travel.starting_point_id"})
    end_point: "Point" = Relationship(sa_relationship_kwargs={"foreign_keys": "Travel.end_point_id"})
    driver: "User" = Relationship()
    passengers: list["User"] = Relationship(back_populates="travels", link_model=TravelUserLink)

    @field_validator('date')
    def date_travel_should_not_be_too_early(cls, v):
        if v >= datetime.now() + timedelta(hours=1):
            raise ValueError('The date of the trip must be an hour later than the current time. / Дата поездки должна '
                             'быть позже текущего времени на час.')
        return v

    @field_validator('number_of_available_seats')
    def number_of_available_seats_must_not_be_equal_zero(cls, v):
        if v == 0:
            raise ValueError('Number of available seats must not be equal zero. / Число свободных мест не должно быть '
                             'равно нулю.')
        return v

    @model_validator(mode='before')
    def check_points(self):
        if self.starting_point_id == self.end_point_id:
            raise ValueError('The point of departure cannot be equal to the point of arrival. / Точка отправления не '
                             'может быть равна точке прибытия')
        return self

    @model_validator(mode='before')
    def set_current_seats(self):
        if self.number_of_available_seats is None:
            raise ValueError("number_of_available_seats не может быть None")
        self.current_number_of_available_seats = self.number_of_available_seats
        return self