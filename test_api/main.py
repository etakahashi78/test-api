import logging

from fastapi import FastAPI

from test_api.routers import image

app = FastAPI()
app.include_router(image.router)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
