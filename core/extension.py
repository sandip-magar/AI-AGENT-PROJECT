from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format= "%(asctime)s -%(levelname)s -%(message)s"
)

#Function to handle the HTTPException handler 
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f" HTTPException error occur on {request.url.path} : {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "detail": exc.detail
            }
        },
    )

async def validation_error_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error occur on {request.url.path}: {exc.errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "success": False,
            "error":{
                "code": 422,
                "message": "Validation error",
                "detail": jsonable_encoder(exc.errors())
            }
        },
    )

async def Server_error_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected error occour on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error":{
                "code": 500,
                "detail": "Internal Server Error"
            }
        }
    )