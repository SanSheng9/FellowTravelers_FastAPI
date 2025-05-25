import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import init_db

from app.routes.users import router as users_routers
from app.routes.regions import router as regions_routers
from app.routes.points import router as points_routers
from app.routes.travels import router as travels_routers
from app.test_data import router as test_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI()

app.include_router(users_routers)
app.include_router(regions_routers)
app.include_router(points_routers)
app.include_router(travels_routers)
app.include_router(test_data)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)