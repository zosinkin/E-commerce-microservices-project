import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


logger = logging.getLogger(__name__)



async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning("HTTPException on %s: %s", request.url.path, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation error on %s: %s", request.url.path, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation error",
            "details": exc.errors(),
            "path": str(request.url.path),
        },
    )

async def unexpected_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "path": str(request.url.path),
        }
    )