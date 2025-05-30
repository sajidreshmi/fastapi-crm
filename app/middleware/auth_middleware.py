from fastapi import Request, HTTPException, status
from typing import Callable


async def auth_middleware(request: Request, call_next: Callable):
    # This is a placeholder for actual authentication logic.
    # In a real application, you would validate tokens, session IDs, etc.
    # For demonstration, let's assume a simple check.
    # If the path is /docs or /redoc, skip authentication
    if request.url.path in ["/docs", "/redoc", "/openapi.json", "/token", "/"]:
        response = await call_next(request)
        return response

    # Example: Check for a custom header for authentication
    if "Authorization" not in request.headers:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    # You can add more complex logic here, e.g., token validation with a database or external service
    # user_token = request.headers["X-Auth-Token"]
    # if not is_valid_token(user_token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

    response = await call_next(request)
    return response
