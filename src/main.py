from fastapi import FastAPI
from src.middlewares import setup_middlewares

app = FastAPI()

setup_middlewares(app)
