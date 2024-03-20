import inspect
from functools import wraps
from typing import Callable, Coroutine, Self

from asgiref.sync import sync_to_async
from django.db.transaction import Atomic


class AsyncAtomic(Atomic):
    def __init__(self, using=None, savepoint=True, durable=False) -> None:
        super().__init__(using, savepoint, durable)

    async def __aenter__(self) -> Self:
        await sync_to_async(super().__enter__)()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await sync_to_async(super().__exit__)(exc_type, exc_value, traceback)


def aatomic(fn: Coroutine | None = None, *args, **kwargs) -> Callable:
    is_coroutine = inspect.iscoroutine(fn)

    if fn is not None and not is_coroutine:
        raise TypeError(f"{fn} is not a coroutine function")

    def wrapper(_fn: Coroutine):
        @wraps(_fn)
        async def _deco(*args, **kwargs):
            async with AsyncAtomic(*args, **kwargs):
                return await _fn(*args, **kwargs)

        return _deco

    if is_coroutine:
        return wrapper(fn)

    return AsyncAtomic(*args, **kwargs)
