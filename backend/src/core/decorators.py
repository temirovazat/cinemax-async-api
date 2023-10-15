import logging
import time
from functools import wraps
from typing import Any, Callable


def backoff(errors: tuple, start_sleep_time=0.1, factor=2, border_sleep_time=10) -> Callable:
    """
    Retry a function after a delay if an error occurs using a decorator.

    Args:
        errors (tuple): Errors to be handled.
        start_sleep_time (float): Initial retry delay.
        factor (float): Multiplier for increasing the delay.
        border_sleep_time (float): Maximum retry delay.

    Returns:
        Callable: Decorated function.
    """
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = start_sleep_time
            while True:
                try:
                    conn = func(*args, **kwargs)
                except errors as message:
                    logging.error(f'Connection failed: {message}!')
                    if delay < border_sleep_time:
                        delay *= factor
                    logging.error(f'Retrying connection in {delay} seconds.')
                    time.sleep(delay)
                else:
                    return conn
        return wrapper
    return decorator
