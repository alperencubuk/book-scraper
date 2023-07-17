from pydantic import BaseModel, ConfigDict, Field

from source.app.books.enums import Order, Sort, Source
from source.core.schemas import PageModel, ResponseModel


class BookModel(BaseModel):
    title: str | None
    publisher: str | None
    writers: list | None
    price: str | None
    url: str | None


class BookRequest(BaseModel):
    source: Source

    model_config = ConfigDict(use_enum_values=True)


class BookResponse(ResponseModel, BookModel):
    pass


class BookPage(PageModel):
    books: list[BookResponse]


class BookPagination(BookRequest):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=0)
    sort: Sort = Sort.ID
    order: Order = Order.ASC
