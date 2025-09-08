from typing import Self

from pydantic import BaseModel, EmailStr, Field, model_validator

from src.core.exception_handlers import ErrorCode, ValidationException


class SignUpRequest(BaseModel):
    email: EmailStr = Field(..., description="유저 이메일")
    username: str = Field(..., min_length=2, max_length=30, description="유저 닉네임")
    password: str = Field(..., min_length=8, max_length=100, description="비밀번호")
    confirm_password: str = Field(..., description="비밀번호 확인")

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValidationException(error_code=ErrorCode.INVALID_PASSWORD)
        return self
