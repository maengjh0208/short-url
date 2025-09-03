from fastapi import FastAPI
from sqlalchemy import select

from src.core.database import get_async_session
from src.models.models import Users

app = FastAPI()


@app.get("/health-check")
async def health_check():
    # TODO: DB 조회 테스트
    async with get_async_session() as session:
        query = select(Users).where(Users.id == 1)
        result = await session.execute(query)
        user = result.scalar()
        print(user)

    return {"status": "Success!"}
