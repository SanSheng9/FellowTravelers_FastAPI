from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///app/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]