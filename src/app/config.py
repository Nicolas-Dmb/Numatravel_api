import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address

load_dotenv(find_dotenv())

bearer_scheme = HTTPBearer()

limiter = Limiter(key_func=get_remote_address)


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.environ.get("CORS_ORIGINS", "").split(","),
        allow_credentials=False,
        allow_methods=["POST"],
        allow_headers=["Content-Type", "Authorization"],
    )
