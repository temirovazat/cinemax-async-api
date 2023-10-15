import logging
from http import HTTPStatus
from typing import Callable

import jwt
import uvicorn
from fastapi import Depends, FastAPI, Header, Request, Response
from fastapi.responses import ORJSONResponse

from api.views import router
from core.config import CONFIG
from core.logger import LOGGING, RequestIdFilter
from db import connections


async def logging_request_id(request_id: str = Header(default=None, alias='X-Request-Id')):
    """Add request ID information to the log for the given request.

    Args:
        request_id (str): The X-Request-Id passed in the request header.
    """
    logger = logging.getLogger('uvicorn.access')
    logger.addFilter(RequestIdFilter(request_id))


app = FastAPI(
    title=CONFIG.fastapi.project_name,
    description='Information about movies, genres, and people involved in creating works',
    version='1.0.0',
    docs_url=f'/{CONFIG.fastapi.docs}',
    openapi_url=f'/{CONFIG.fastapi.docs}.json',
    default_response_class=ORJSONResponse,
    dependencies=[Depends(logging_request_id)],
)


@app.on_event('startup')
async def startup():
    """Connect to databases when the server starts."""
    await connections.start_redis()
    await connections.start_elasticsearch()
    await connections.create_genres_index()
    await connections.create_persons_index()
    await connections.create_movies_index()


@app.middleware('http')
async def access_control(request: Request, call_next: Callable) -> Response:
    """Manage access to resources.

    Args:
        request (Request): The client's request.
        call_next (Callable): The request handler function.

    Returns:
        Response: The server's response.
    """
    url_path, headers = request.scope['path'], request.headers
    if url_path in {app.docs_url, f'{app.docs_url}/', app.openapi_url}:
        return await call_next(request)
    if CONFIG.fastapi.debug is False and url_path != request.app.url_path_for('films'):
        try:
            jwt.decode(
                jwt=headers['authorization'].split()[1],
                key=CONFIG.fastapi.secret_key,
                algorithms=['HS256'],
            )
        except KeyError:
            return Response('Access is restricted to authorized users only!', status_code=HTTPStatus.UNAUTHORIZED)
        except jwt.ExpiredSignatureError:
            return Response('Session has expired!', status_code=HTTPStatus.UNAUTHORIZED)
        except Exception as exc:
            logging.error(f'Issue with user authorization: {exc}!')
            return Response('Technical maintenance is in progress!', status_code=HTTPStatus.BAD_REQUEST)
    return await call_next(request)


@app.on_event('shutdown')
async def shutdown():
    """Disconnect from databases when the server shuts down."""
    await connections.stop_redis()
    await connections.stop_elasticsearch()


app.include_router(router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=CONFIG.fastapi.host,
        port=CONFIG.fastapi.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
