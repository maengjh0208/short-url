from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import users


def create_app() -> FastAPI:
    app = FastAPI()

    # Static
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    # Router
    app.include_router(users.router, prefix="/users", tags=["users"])

    return app


app = create_app()


@app.get("/health-check")
async def health_check():
    # # TODO: DB 조회 테스트
    # async with get_async_session() as session:
    #     query = select(Users).where(Users.id == 1)
    #     result = await session.execute(query)
    #     user = result.scalar()
    #     print(user)

    return {"status": "Success!"}
