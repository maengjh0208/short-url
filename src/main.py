from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.exception_handlers import setup_exception_handlers
from src.core.middleware import authenticate_request
from src.routers import users


def create_app() -> FastAPI:
    app = FastAPI()

    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    app.include_router(users.router, prefix="/users", tags=["users"])

    app.middleware("http")(authenticate_request)

    setup_exception_handlers(app)

    return app


app = create_app()


@app.get("/health-check")
async def health_check():
    return {"status": "Success!"}
