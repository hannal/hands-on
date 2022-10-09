from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


async def validation_exception_handler(
    request: Request, exc: ValidationError | RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.json(),
    )


def setup_error_handlers(_app):
    _app.exception_handler(ValidationError)(validation_exception_handler)
    _app.exception_handler(RequestValidationError)(validation_exception_handler)
