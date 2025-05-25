from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.database import SessionDep
from app.models.regions import Region
from app.models.users import User, UserCreate, UserPublic, UserPublicWithRegion, UserUpdate

router = APIRouter()

@router.post("/users/", response_model=UserPublic, tags=["users"])
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/users/", response_model=list[UserPublic], tags=["users"])
def read_users(session: SessionDep, chat_id: Optional[int] = None):
    query = select(User)
    if chat_id is not None:
        query = query.where(User.chat_id == chat_id)
    users = session.exec(query).all()
    return users

@router.get("/users/{user_id}", response_model=UserPublicWithRegion, tags=["users"])
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/users/{user_id}", response_model=UserPublicWithRegion, tags=["users"])
def change_user(user_id: int, user_update: UserUpdate, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    region = session.get(Region, user_update.region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    user.region = region
    session.add(user)
    session.commit()
    session.refresh(user)

    return user