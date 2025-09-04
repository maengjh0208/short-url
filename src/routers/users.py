from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from src.core.templates import templates

router = APIRouter()


@router.get(
    "/login",
    description="로그인 및 회원가입 페이지",
    response_class=HTMLResponse,
)
async def show_login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="auth.html")
