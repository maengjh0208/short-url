from typing import Annotated

from fastapi import APIRouter, Form, Request
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from src.core.config import settings
from src.core.templates import templates
from src.schemas.users import LoginRequest, SignUpRequest
from src.services.users import user_service

router = APIRouter()


@router.get(
    "/login",
    description="로그인 및 회원가입 페이지",
    response_class=HTMLResponse,
)
async def get_login_and_signup_page(
    request: Request,
    is_signup_success: bool = False,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="login_and_signup.html",
        context={
            "message": "회원가입이 완료되었습니다. 로그인해주세요." if is_signup_success else None,
        },
    )


@router.post(
    "/login",
    description="로그인 요청",
    response_class=RedirectResponse,
)
async def login(form_data: Annotated[LoginRequest, Form()]) -> RedirectResponse:
    result = await user_service.login(
        email=form_data.email,
        password=form_data.password,
    )

    # TODO: 경로 / 인 메인 페이지 추가해야 함
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    # TODO: 토큰 관리는 추후 middleware 같은 곳으로 옮겨야 하지 않을까
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        samesite="lax",
    )

    return response


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

    return RedirectResponse(url="/users/login?is_signup_success=true", status_code=status.HTTP_302_FOUND)
