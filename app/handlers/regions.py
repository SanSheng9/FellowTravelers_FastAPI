from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.database import SessionDep
from app.models.regions import Region
from app.schemes.regions import RegionPublic, RegionCreate

router = APIRouter()

@router.post("/regions/", response_model=RegionPublic, tags=["regions"])
def create_region(region: RegionCreate, session: SessionDep):
    db_region = Region.model_validate(region)
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region

@router.get("/regions/", response_model=list[RegionPublic], tags=["regions"])
def read_regions(session: SessionDep):
    regions = session.exec(select(Region)).all()
    return regions

@router.get("/regions/{region_id}", response_model=RegionPublic, tags=["regions"])
def read_region(region_id: int, session: SessionDep):
    region = session.get(Region, region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Hero not found")
    return region