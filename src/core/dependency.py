from starlette.requests import Request

from src.core.exception_handlers import AuthenticationException, ErrorCode


def get_current_user(request: Request) -> dict:
    user = getattr(request.state, "user", None)

    if not user:
        raise AuthenticationException(error_code=ErrorCode.UNAUTHORIZED)

    return user
