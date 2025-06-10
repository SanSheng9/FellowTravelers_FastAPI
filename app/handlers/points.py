from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.database import SessionDep
from app.models.points import Point
from app.schemes.points import PointPublic, PointCreate, PointPublicWithRegion

router = APIRouter()

@router.post("/points/", response_model=PointPublic, tags=["points"])
def create_point(point: PointCreate, session: SessionDep):
    db_point = Point.model_validate(point)
    session.add(db_point)
    session.commit()
    session.refresh(db_point)
    return db_point

@router.get("/points/", response_model=list[PointPublicWithRegion], tags=["points"])
def read_points(session: SessionDep):
    query = select(Point).join(Point.region).options(joinedload(Point.region))
    points = session.exec(query).all()
    return points

@router.get("/points/{point_id}", response_model=PointPublicWithRegion, tags=["points"])
def read_point(*, point_id: int, session: SessionDep):
    query = select(Point).options(joinedload(Point.region)).where(Point.id == point_id)
    point = session.exec(query).first()
    if not point:
        raise HTTPException(status_code=404, detail="Hero not found")
    return point