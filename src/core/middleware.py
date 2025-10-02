from starlette.requests import Request

from src.core.database import get_async_session
from src.repositories.users import UserRepository
from src.utils.auth import verify_token


async def authenticate_request(request: Request, call_next):
    """
    JWT 토큰 검증 미들웨어

    작동 방식:
    1. 쿠키에서 토큰 추출
    2. 토큰 검증
    3. request.state 에 검증된 사용자 정보 저장
    """

    exclude_paths = [
        "/health-check",
        "/users/login",
        "/users/signup",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    ]

    request.state.user = None

    if request.url.path in exclude_paths or "/static" in request.url.path:
        return await call_next(request)

    access_token = request.cookies.get("access_token")
    # refresh_token = request.cookies.get("refresh_token")

    # TODO: refresh_token 으로 access_token 자동 갱신 만들어줘야함.
    if not access_token:
        return await call_next(request)

    payload = verify_token(access_token)

    if not payload:
        return await call_next(request)

    try:
        user_id = int(payload.get("sub"))
        user_email = payload.get("email")

        async with get_async_session() as session:
            user_repo = UserRepository()
            user_info = await user_repo.get_user_by_id(session=session, user_id=user_id)

            if user_info and user_info.email == user_email:
                request.state.user = {
                    "id": user_info.id,
                    "email": user_info.email,
                    "username": user_info.username,
                }

    except Exception:
        # TODO: Exception e 로그
        pass

    return await call_next(request)
