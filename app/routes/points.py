from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.database import SessionDep
from app.models.points import PointPublic, Point, PointCreate, PointPublicWithRegion

router = APIRouter()

@router.post("/points/", response_model=PointPublic, tags=["points"])
def create_point(point: PointCreate, session: SessionDep):
    db_point = Point.model_validate(point)
    session.add(db_point)
    session.commit()
    session.refresh(db_point)
    return db_point

@router.get("/points/", response_model=list[PointPublicWithRegion], tags=["points"])
def read_points(session: SessionDep, region_id: Optional[int] = None):
    query = select(Point).join(Point.region).options(joinedload(Point.region))
    if region_id is not None:
        query = query.where(Point.region_id == region_id)
    points = session.exec(query).all()
    return points

@router.get("/points/{point_id}", response_model=PointPublicWithRegion, tags=["points"])
def read_point(*, point_id: int, session: SessionDep):
    point = session.get(Point, point_id)
    if not point:
        raise HTTPException(status_code=404, detail="Hero not found")
    return point