import time
from fastapi import Request


async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(
        f"Request: {request.method} {request.url.path} - Processed in: {process_time:.4f}s")
    return response
