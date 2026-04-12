import logging

from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler

from .config import limiter, setup_cors
from .router import router

logging.basicConfig(level=logging.INFO)
logging.info("Starting the application...")

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

setup_cors(app)
app.include_router(router)
