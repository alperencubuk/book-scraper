from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from source.core.settings import settings

api_key = APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)


async def api_key_auth(
    api_key_header: str = Security(api_key),
):
    if api_key_header == settings.API_KEY:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Api Key."
    )
