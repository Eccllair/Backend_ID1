import logging

from fastapi import FastAPI, Request
from datetime import datetime, timedelta
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import StreamingResponse

from .routers.chat_router import chat_router
from .routers.user_router import users_router
from .routers.serving_router import serving_router
from .routers.product_router import product_router, product_download_router

app = FastAPI()

logging.basicConfig(filename=r'idz\fastapi.log', level=logging.INFO)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)

@app.middleware("http")
async def log_queries(request: Request, call_next):
    start_time = datetime.now()
    response: StreamingResponse = await call_next(request)
    process_time = datetime.now() - start_time
    logging.info(f"{start_time.hour}:{start_time.minute}:{start_time.second}\nrequest method: {request.method} request url: {request.url.path}\nprocess time = {process_time.seconds} seconds {process_time.microseconds} microseconds\n")
    
    return response

app.include_router(
    router=users_router,
    prefix="/users"
)

app.include_router(
    router=chat_router,
    prefix="/chats"
)

app.include_router(
    router=serving_router
)

app.include_router(
    router=product_router,
    prefix="/products"
)

app.include_router(
    router=product_download_router,
    prefix="/products_download"
)