from typing import Annotated

from fastapi import APIRouter, Form, Request
from starlette.responses import HTMLResponse

from src.core.templates import templates
from src.schemas.users import SignUpRequest
from src.services.users import user_service

router = APIRouter()


@router.get(
    "/login",
    description="로그인 및 회원가입 페이지",
    response_class=HTMLResponse,
)
async def show_login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="auth.html")


@router.post(
    "/signup",
    description="회원 가입",
)
async def signup(form_data: Annotated[SignUpRequest, Form()]):
    await user_service.signup(
        email=form_data.email,
        username=form_data.username,
        password=form_data.password,
    )
