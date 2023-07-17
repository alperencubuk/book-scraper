from asyncio import gather
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from source.core.database import create_index, database_health
from source.core.jobs import scheduler
from source.core.routers import api_router
from source.core.schemas import HealthModel
from source.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await gather(create_index())
    scheduler.start()
    yield


app = FastAPI(title=settings.APP_TITLE, version=settings.VERSION, lifespan=lifespan)

app.include_router(api_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthModel, tags=["health"])
async def health_check():
    return {"api": True, "database": await database_health()}
