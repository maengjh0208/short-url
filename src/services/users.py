from src.core.database import get_async_session
from src.core.exception_handlers import AuthenticationException, DuplicateException, ErrorCode
from src.repositories.users import UserRepository
from src.schemas.users import LoginResponse
from src.utils.auth import create_access_token, create_refresh_token, hash_password, verify_password


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def signup(self, email: str, username: str, password: str) -> None:
        async with get_async_session() as session:
            if await self.user_repo.get_user_by_email(session=session, email=email):
                raise DuplicateException(error_code=ErrorCode.DUPLICATED_EMAIL)

            hashed_password = hash_password(password)
            await self.user_repo.create_user(session, email, username, hashed_password)

    async def login(self, email: str, password: str) -> LoginResponse:
        async with get_async_session() as session:
            user = await self.user_repo.get_user_by_email(session=session, email=email)
            if not user:
                raise AuthenticationException(error_code=ErrorCode.UNAUTHORIZED_LOGIN)

            if not verify_password(password, user.hashed_password):
                raise AuthenticationException(error_code=ErrorCode.UNAUTHORIZED_LOGIN)

            token_data = {"sub": str(user.id), "email": user.email}
            access_token = create_access_token(token_data)
            refresh_token = create_refresh_token(token_data)

            if await self.user_repo.get_refresh_token(session, user.id):
                await self.user_repo.update_refresh_token(session=session, user_id=user.id, refresh_token=refresh_token)
            else:
                await self.user_repo.create_refresh_token(session=session, user_id=user.id, refresh_token=refresh_token)

            return LoginResponse(
                access_token=access_token,
                refresh_token=refresh_token,
            )


user_service = UserService()
