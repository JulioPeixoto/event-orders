from fastapi import FastAPI
from src.middlewares.cors import setup_cors


def setup_middlewares(app: FastAPI) -> None:
    setup_cors(app)
