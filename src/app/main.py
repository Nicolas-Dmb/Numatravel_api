import logging

from fastapi import FastAPI
from router import router

logging.basicConfig(level=logging.INFO)
logging.info("Starting the application...")

app = FastAPI()
app.include_router(router)
