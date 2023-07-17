from apscheduler.schedulers.asyncio import AsyncIOScheduler

from source.app.books.enums import Source
from source.app.books.services import crawl_books
from source.core.database import database


async def crawl_kitapsepeti() -> None:
    await crawl_books(Source.KITAPSEPETI, database)
    return None


async def crawl_kitapyurdu() -> None:
    await crawl_books(Source.KITAPYURDU, database)
    return None


scheduler = AsyncIOScheduler()

scheduler.add_job(crawl_kitapsepeti, "cron", hour=0)
scheduler.add_job(crawl_kitapyurdu, "cron", hour=1)
