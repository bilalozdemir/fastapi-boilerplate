import time
import logging

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from fastapi import Depends, FastAPI, Request

from src.routers import router

app = FastAPI()

app.include_router(router.router)

## Middlewares

@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

## Root APIs

@app.get("/health")
async def health_check():
    return {"health": "ok"}
