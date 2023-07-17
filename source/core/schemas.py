from pydantic import BaseModel


class ResponseModel(BaseModel):
    pass


class PageModel(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class HealthModel(BaseModel):
    api: bool
    database: bool


class GeneralModel(BaseModel):
    detail: str
