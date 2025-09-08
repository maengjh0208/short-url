from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exception_handlers import InternalServerException
from src.models.models import Users


@dataclass
class UserDTO:
    id: int
    email: str
    username: str
    hashed_password: str


class UserRepository:
    async def get_by_email(self, session: AsyncSession, email: str) -> UserDTO:
        query = select(
            Users.id,
            Users.email,
            Users.name,
            Users.hashed_password,
        ).where(Users.email == email)

        result = await session.execute(query)
        result = result.one_or_none()

        return (
            UserDTO(
                id=result.id,
                email=result.email,
                username=result.name,
                hashed_password=result.hashed_password,
            )
            if result
            else None
        )

    async def create_user(self, session: AsyncSession, email: str, username: str, hashed_password: str) -> None:
        try:
            user = Users(
                email=email,
                name=username,
                hashed_password=hashed_password,
            )

            session.add(user)
            await session.flush()
        except Exception as e:
            raise InternalServerException(detail={"message": e.args[0]})
