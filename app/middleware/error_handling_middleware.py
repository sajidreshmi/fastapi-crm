from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse


async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code,
            content={"detail": http_exc.detail}
        )
    except Exception as e:
        # Log the unexpected error
        print(f"An unexpected error occurred: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )
