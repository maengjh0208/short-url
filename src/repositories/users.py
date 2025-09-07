from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Users


@dataclass
class UserDTO:
    id: int
    email: str
    username: str
    hashed_password: str


class UserRepository:
    async def get_by_email(self, session: AsyncSession, email: str):
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
            # TODO: 에러를 상위 함수로 전달하는 것과 별개로, 에러가 발생된 메서드에서 발생 원인을 로깅 해줘야 할 것 같다.
            raise Exception(f"회원 생성 실패 || ERROR: {e}")
