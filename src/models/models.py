import datetime
from typing import List

from sqlalchemy import TIMESTAMP, ForeignKeyConstraint, Index, Integer, String, Text, inspect, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    def __repr__(self):
        class_name = self.__class__.__name__

        inspector = inspect(self.__class__)
        columes = inspector.columns.keys()

        attrs = []
        for colume in columes:
            value = getattr(self, colume, None)

            if isinstance(value, str):
                attrs.append(f"{colume}='{value}'")
            else:
                attrs.append(f"{colume}={value}")

        attrs_str = ", ".join(attrs)
        return f"<{class_name}({attrs_str})>"


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (Index("email", "email", unique=True),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255, "utf8mb4_unicode_ci"))
    name: Mapped[str] = mapped_column(String(100, "utf8mb4_unicode_ci"))
    hashed_password: Mapped[str] = mapped_column(String(255, "utf8mb4_unicode_ci"))
    is_active: Mapped[int] = mapped_column(TINYINT(1), server_default=text("'1'"))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    refresh_tokens: Mapped[List["RefreshTokens"]] = relationship("RefreshTokens", back_populates="user")


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE", onupdate="CASCADE", name="fk_refresh_tokens_user_id"
        ),
        Index("idx_expires_at", "expires_at"),
        Index("idx_is_active", "is_active"),
        Index("idx_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    refresh_token: Mapped[str] = mapped_column(Text(collation="utf8mb4_unicode_ci"))
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    is_active: Mapped[int] = mapped_column(TINYINT(1), server_default=text("'1'"))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    user: Mapped["Users"] = relationship("Users", back_populates="refresh_tokens")
