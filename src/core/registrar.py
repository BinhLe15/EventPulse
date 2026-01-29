from starlette.middleware.gzip import GZipMiddleware
from src.api.v1.api import api_router
from src.rate_limiter import limiter
from src.core.config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler



def custom_generate_unique_id(route: APIRoute) -> str:
    if route.tags and len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"

    else:
        # Fallback for routes without tags
        return f"default-{route.name}"


def register_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        generate_unique_id_function=custom_generate_unique_id,
    )

    register_router(app)
    register_middleware(app)
    add_app_states(app)

    return app


def register_middleware(app: FastAPI):
    app.add_middleware(SlowAPIMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS.replace(" ", "").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(GZipMiddleware)


def register_router(app: FastAPI):
    app.include_router(api_router)


def add_app_states(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
