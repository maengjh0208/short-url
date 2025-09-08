from src.core.database import get_async_session
from src.core.exception_handlers import DuplicateException, ErrorCode
from src.repositories.users import UserRepository
from src.utils.jwt import hash_password


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def signup(self, email: str, username: str, password: str) -> None:
        async with get_async_session() as session:
            if await self.user_repo.get_by_email(session, email):
                raise DuplicateException(error_code=ErrorCode.DUPLICATED_EMAIL)

            hashed_password = hash_password(password)
            await self.user_repo.create_user(session, email, username, hashed_password)


user_service = UserService()
