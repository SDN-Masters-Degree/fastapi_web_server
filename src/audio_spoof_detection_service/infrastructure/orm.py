from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class BaseOrm(DeclarativeBase):
    pass


class UserOrm(BaseOrm):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    refresh_token: Mapped[str | None] = mapped_column(String(32), nullable=True)
    refresh_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)


class OneTimePasswordOrm(BaseOrm):
    __tablename__ = 'one_time_password'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('UserOrm.id'), nullable=False)
    password: Mapped[str] = mapped_column(String(10), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)


class AudioMetaInfoOrm(BaseOrm):
    __tablename__ = 'audio_meta_info'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('UserOrm.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    analyze_result: Mapped[str | None] = mapped_column(String(10), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
