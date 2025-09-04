from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from src.core.database import get_async_session
from src.models.models import Users

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")


@app.get("/health-check")
async def health_check():
    # TODO: DB 조회 테스트
    async with get_async_session() as session:
        query = select(Users).where(Users.id == 1)
        result = await session.execute(query)
        user = result.scalar()
        print(user)

    return {"status": "Success!"}


@app.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={"id": 100, "name": "test"},
    )
