from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        print(f"IntegrityError: {exc}")
        return JSONResponse(
            status_code=409,
            content={"error": "Integrity constraint violation", "details": str(exc.orig)}

        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        print(f"UnexpectedError: {exc}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "details": str(exc)}
        )
