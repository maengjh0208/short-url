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
    try:
        await user_service.signup(
            email=form_data.email,
            username=form_data.username,
            password=form_data.password,
        )

        # TODO: 회원가입이 완료되었다는 Template 을 노출
    except Exception:
        # TODO: 회원가입이 실패되었다는 Template 을 노출
        raise Exception("회원가입 실패!")
