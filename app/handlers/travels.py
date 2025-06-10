import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.database import SessionDep
from app.models.travels import Travel, TravelUserLink
from app.schemes.travels import TravelPublic, TravelCreate, TravelUserCreate, TravelUserPublic

router = APIRouter()

"""
Нужны проверки:
1. Дата поездки больше текущей.
2. Точки не равняются друг другу и находятся в пределах региона водителя.
"""

@router.post("/travels/", response_model=TravelPublic, tags=["travels"])
def create_travel(travel: TravelCreate, session: SessionDep):
    db_travel = Travel.model_validate(travel)
    session.add(db_travel)
    session.commit()
    session.refresh(db_travel)
    return db_travel

@router.get("/travels/", response_model=list[TravelPublic], tags=["travels"])
def read_travels(session: SessionDep,
                 starting_point_id: int = None,
                 end_point_id: int = None,
                 date: str = None): # формат "YYYY-MM-DD"

    if starting_point_id and end_point_id and date:
        try:
            filter_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        travels = session.exec(
            select(Travel)
            .options(
                joinedload(Travel.starting_point),
                joinedload(Travel.end_point),
                joinedload(Travel.driver)
            )
            .where(Travel.starting_point_id == starting_point_id)
            .where(Travel.end_point_id == end_point_id)
            .where(func.date(Travel.date) == filter_date)
        ).all()

    else:
        travels = session.exec(select(Travel)).all()

    return travels

@router.get("/travels/{travel_id}", response_model=TravelPublic, tags=["travels"])
def read_travel(travel_id: int, session: SessionDep):
    travel = session.get(Travel, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="Hero not found")
    return travel

@router.post("/travels/{travel_id}/add_passenger/", response_model=TravelUserPublic, tags=["travels"])
def add_passenger(travel_id: int, passenger: TravelUserCreate, session: SessionDep):
    db_passenger = TravelUserLink(**passenger.model_dump(), travel_id=travel_id)
    session.add(db_passenger)
    session.commit()
    session.refresh(db_passenger)
    return db_passenger

@router.get("/travels/{travel_id}/passengers/", response_model=list[TravelUserPublic], tags=["travels"])
def read_passengers(travel_id: int, session: SessionDep):
    passengers = session.exec(select(TravelUserLink).where(TravelUserLink.travel_id == travel_id)).all()
    return passengers