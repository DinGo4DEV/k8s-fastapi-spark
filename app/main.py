import logging
import os
import sys
from importlib import import_module
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import PlainTextResponse, UJSONResponse
from pydantic import ValidationError
from redis.asyncio import Redis
from starlette_exporter import PrometheusMiddleware, handle_metrics
from . import logger
from app.routers import *


def metrics_filter(record):
    if "/metrics" in record.args:
        return False
    return True


logging.getLogger("uvicorn.access").addFilter(metrics_filter)
logger.info("start main.py")
# ARANGO_CONFIG = config['datasource']['ARANGO']
# client = ArangoClient(hosts=ARANGO_CONFIG["url"],http_client=HTTPClient())


app = FastAPI(
    title="K8s Spark Service",
    description="",
    default_response_class=UJSONResponse,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origin_regex="https?://.*\.devhk\.dev(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    PrometheusMiddleware,
    app_name="epc-account-management",
    prefix="fastapi",
    skip_paths=[
        f'{f"/{app.root_path}" if app.root_path else ""}/metrics',
        f'{f"/{app.root_path}" if app.root_path else ""}/openapi.json',
    ],
    filter_unhandled_paths=False,
    group_paths=True,
    always_use_int_status=True,
)

## Prometheus Metrics Route
app.add_route("/metrics", handle_metrics)

# @app.on_event("startup")
# async def startup():
#     redis = Redis.from_url(
#         f"redis://{config['redis']['host']}:{config['redis']['port']}",
#         encoding="utf8",
#         decode_responses=True,
#     )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return PlainTextResponse(exc.json(), status_code=422)


## dynamic add routers (files inside routers & `router` object)
from fastapi import APIRouter

routers = list(filter(lambda module: "router" in module, sys.modules))
for router in routers:
    module = sys.modules[router]
    for path in module.__path__:
        for obj in os.scandir(path):
            if obj.is_file() and "__init__" not in obj.name:
                module = import_module("." + obj.name[:-3], package=router)
                app_router = getattr(module, "router", None)
                if app_router and isinstance(app_router, APIRouter):
                    app.include_router(app_router)

## use the following command to start fastapi
## uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
