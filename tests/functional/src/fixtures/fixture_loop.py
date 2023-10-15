import asyncio
from typing import Iterator

import pytest


@pytest.fixture(scope='session')
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """
    Get a new `event_loop` object for proper asynchronous code execution.

    Yields:
        asyncio.AbstractEventLoop: The `event_loop` object.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()
