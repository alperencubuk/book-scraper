from fastapi import APIRouter, Depends, status
from fastapi.background import BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase

from source.app.books.schemas import BookPage, BookPagination, BookRequest
from source.app.books.services import crawl_books, list_books
from source.core.database import get_db
from source.core.schemas import GeneralModel

books_router = APIRouter(prefix="/books")


@books_router.post(
    "/",
    response_model=GeneralModel,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": GeneralModel}},
    tags=["books"],
)
async def book_crawl(
    request: BookRequest,
    background_tasks: BackgroundTasks,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> GeneralModel:
    background_tasks.add_task(crawl_books, request.source, db)
    return GeneralModel(detail=f"Crawl started for source: {request.source}")


@books_router.get(
    "/",
    response_model=BookPage,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": GeneralModel}},
    tags=["books"],
)
async def book_list(
    pagination: BookPagination = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> BookPage:
    return await list_books(
        page=pagination.page,
        size=pagination.size,
        sort=pagination.sort,
        order=pagination.order,
        source=pagination.source,
        db=db,
    )
