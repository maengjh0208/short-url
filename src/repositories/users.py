from dataclasses import dataclass

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exception_handlers import InternalServerException
from src.models.models import RefreshTokens, Users


@dataclass
class UserDTO:
    id: int
    email: str
    username: str
    hashed_password: str


@dataclass
class RefreshTokenDTO:
    id: int
    refresh_token: str


class UserRepository:
    async def get_user_by_email(self, session: AsyncSession, email: str) -> UserDTO:
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

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> UserDTO:
        query = select(
            Users.id,
            Users.email,
            Users.name,
            Users.hashed_password,
        ).where(Users.id == user_id)

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
            raise InternalServerException(detail={"message": str(e)})

    async def get_refresh_token(self, session: AsyncSession, user_id: int) -> RefreshTokenDTO:
        query = select(
            RefreshTokens.id,
            RefreshTokens.refresh_token,
        ).where(RefreshTokens.user_id == user_id)

        result = await session.execute(query)
        result = result.one_or_none()

        return (
            RefreshTokenDTO(
                id=result.id,
                refresh_token=result.refresh_token,
            )
            if result
            else None
        )

    async def create_refresh_token(self, session: AsyncSession, user_id: int, refresh_token: str):
        try:
            refresh_token = RefreshTokens(
                user_id=user_id,
                refresh_token=refresh_token,
            )

            session.add(refresh_token)
            await session.flush()
        except Exception as e:
            raise InternalServerException(detail={"message": str(e)})

    async def update_refresh_token(
        self,
        session: AsyncSession,
        user_id: int,
        refresh_token: str | None = None,
    ):
        try:
            query = (
                update(RefreshTokens)
                .where(
                    RefreshTokens.user_id == user_id,
                )
                .values(
                    refresh_token=refresh_token,
                )
            )

            result = await session.execute(query)

            if not result.rowcount:
                raise Exception("토큰 업데이트 실패: 사용자를 찾을 수 없음")

        except Exception as e:
            raise InternalServerException(detail={"message": str(e)})
