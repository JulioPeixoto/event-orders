from fastapi import FastAPI
from src.middlewares import setup_middlewares
from src.modules.users.routes import router as users_router
from src.modules.orders.routes import router as orders_router

app = FastAPI(prefix="/api/v1")

setup_middlewares(app)

app.include_router(users_router)
app.include_router(orders_router)


@app.get("/")
def health_check():
    return {
        "status": "ok",
    }
