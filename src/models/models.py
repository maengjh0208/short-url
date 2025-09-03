import datetime

from sqlalchemy import TIMESTAMP, Index, Integer, String, inspect, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
    email: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[int] = mapped_column(TINYINT(1), server_default=text("'1'"))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
