from enum import Enum
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette import status
from starlette.exceptions import HTTPException

from src.core.templates import templates

""" 에러 코드 정의 """


class ErrorCode(Enum):
    # status code: 400
    INVALID_REQUEST = ("E4000", "잘못된 요청입니다.")

    # status code: 401
    UNAUTHORIZED = ("E4010", "인증이 필요합니다.")

    # status code: 403
    FORBIDDEN = ("E4030", "접근 권한이 없습니다.")

    # status code: 404
    NOT_FOUND = ("E4040", "요청한 리소스를 찾을 수 없습니다.")

    # status code: 409
    DUPLICATED = ("E4090", "이미 존재하는 데이터입니다.")
    DUPLICATED_EMAIL = ("E4091", "이미 존재하는 이메일입니다.")

    # statuscode: 500
    INTERNAL_SERVER_ERROR = ("E5000", "서버에서 예상치 못한 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


""" 예외 처리 관련 클래스 정의 """


class BaseCustomException(Exception):
    """기본 커스텀 예외 클래스"""

    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        detail: Dict[str, Any] | None = None,
    ):
        self.status_code = status_code
        self.error_code = error_code.code
        self.error_message = error_code.message
        self.detail = detail or {}

        super().__init__(self.error_message)


class ValidationException(BaseCustomException):
    """데이터 유효성 검증 관련 예외 클래스"""

    def __init__(
        self,
        error_code: ErrorCode = ErrorCode.INVALID_REQUEST,
        detail: Dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
            detail=detail,
        )


class AuthenticationException(BaseCustomException):
    """인증 관련 예외 클래스"""

    def __init__(
        self,
        error_code: ErrorCode = ErrorCode.UNAUTHORIZED,
        detail: Dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=error_code,
            detail=detail,
        )


class AuthorizationException(BaseCustomException):
    """권한 관련 예외 클래스"""

    def __init__(
        self,
        error_code: ErrorCode = ErrorCode.FORBIDDEN,
        detail: Dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code,
            detail=detail,
        )


class NotFoundException(BaseCustomException):
    """리소스를 찾을 수 없는 예외 클래스"""

    def __init__(
        self,
        error_code: ErrorCode = ErrorCode.NOT_FOUND,
        detail: Dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code,
            detail=detail,
        )


class DuplicateException(BaseCustomException):
    """중복 데이터 예외 클래스"""

    def __init__(
        self,
        error_code: ErrorCode = ErrorCode.DUPLICATED,
        detail: Dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code,
            detail=detail,
        )


class InternalServerException(BaseCustomException):
    """ "내부 서버 예외 클래스"""

    def __init__(
        self,
        error_code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
        detail: Dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
            detail=detail,
        )


""" exception handler 등록 """


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseCustomException)
    async def custom_exception_handler(request: Request, exc: BaseCustomException) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="http_error.html",
            context={
                "status_code": exc.status_code,
                "message": f"{exc.error_code}: {exc.error_message}",
                "detail": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="http_error.html",
            context={
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"{ErrorCode.INVALID_REQUEST.code}: {ErrorCode.INVALID_REQUEST.message}",
                "detail": exc.errors()[0],
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="http_error.html",
            context={
                "status_code": exc.status_code,
                "message": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="http_error.html",
            context={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"{ErrorCode.INTERNAL_SERVER_ERROR.code}: {ErrorCode.INTERNAL_SERVER_ERROR.message}",
                "detail": {
                    "type": type(exc),
                    "message": exc.args[0],
                },
            },
        )
