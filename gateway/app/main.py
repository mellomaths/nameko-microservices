from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import config

from .api.entrypoints import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix=config.get_settings().api_path)

