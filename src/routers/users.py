from typing import Annotated

from fastapi import APIRouter, Form, Query, Request
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from src.core.templates import templates
from src.schemas.users import SignUpRequest
from src.services.users import user_service

router = APIRouter()


@router.get(
    "/login",
    description="로그인 및 회원가입 페이지",
    response_class=HTMLResponse,
)
async def show_login_page(
    request: Request,
    message: Annotated[str | None, Query()] = None,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={
            "message": message,
        },
    )


@router.post(
    "/signup",
    description="회원 가입",
    response_class=RedirectResponse,
)
async def signup(form_data: Annotated[SignUpRequest, Form()]) -> RedirectResponse:
    await user_service.signup(
        email=form_data.email,
        username=form_data.username,
        password=form_data.password,
    )

    return RedirectResponse(
        url="/users/login?message=회원가입이 완료되었습니다.\n로그인해주세요.", status_code=status.HTTP_302_FOUND
    )
