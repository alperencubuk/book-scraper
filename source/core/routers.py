from fastapi import APIRouter, Depends

from source.app.books.views import books_router
from source.core.auth import api_key_auth

api_router = APIRouter()

api_router.include_router(books_router, dependencies=[Depends(api_key_auth)])
