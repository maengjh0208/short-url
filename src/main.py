from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from src.core.database import get_async_session
from src.models.models import Users
from src.routers import users

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/health-check")
async def health_check():
    # TODO: DB 조회 테스트
    async with get_async_session() as session:
        query = select(Users).where(Users.id == 1)
        result = await session.execute(query)
        user = result.scalar()
        print(user)

    return {"status": "Success!"}
