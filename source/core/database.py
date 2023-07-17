from asyncio import gather

from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from source.core.settings import settings

mongo_client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)


def get_db() -> AsyncIOMotorDatabase:
    return mongo_client.smartmaple


database = get_db()


async def create_index() -> None:
    await gather(
        database["kitapyurdu"].create_index("title"),
        database["kitapyurdu"].create_index("url"),
        database["kitapsepeti"].create_index("title"),
        database["kitapsepeti"].create_index("url"),
    )


async def database_health() -> bool:
    try:
        await mongo_client.admin.command("ping")
        return True
    except ConnectionFailure:
        return False
