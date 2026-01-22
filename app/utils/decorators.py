import time
import functools
import logging

def log_execution(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"DEBUG: {func.__name__} executed in {duration:.4f}s")
        return result
    return wrapper