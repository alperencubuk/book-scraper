from math import ceil

from motor.motor_asyncio import AsyncIOMotorDatabase
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.kitapsepeti import KitapSepetiSpider
from scraper.spiders.kitapyurdu import KitapYurduSpider
from source.app.books.enums import Order, Sort, Source
from source.app.books.schemas import BookPage, BookResponse


async def list_books(
    page: int,
    size: int,
    sort: Sort,
    order: Order,
    source: Source,
    db: AsyncIOMotorDatabase,
) -> BookPage:
    sort_by = "_id" if sort == Sort.ID.value else sort
    order_by = 1 if order == Order.ASC.value else -1
    book_list = (
        await db[source]
        .find()
        .sort(sort_by, order_by)
        .skip((page - 1) * size)
        .limit(size)
        .to_list(None)
    )

    book_list = [BookResponse(**book_item).dict() for book_item in book_list]

    total = await db[source].estimated_document_count()

    return BookPage(
        books=book_list,
        page=page,
        size=size,
        total=total,
        pages=(ceil(total / size) if size else 1),
    )


async def crawl_books(source: Source, db: AsyncIOMotorDatabase) -> None:
    process = CrawlerProcess(get_project_settings())
    if source == Source.KITAPSEPETI:
        process.crawl(KitapSepetiSpider, db)
    elif source == Source.KITAPYURDU:
        process.crawl(KitapYurduSpider, db)
    process.start()
