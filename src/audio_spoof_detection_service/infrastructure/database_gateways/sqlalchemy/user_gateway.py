from sqlalchemy import select
from sqlalchemy.orm import Session

from audio_spoof_detection_service.application.protocols.database_gateways.user_gateway import UserGateway
from audio_spoof_detection_service.infrastructure.orm import UserOrm, OneTimePasswordOrm
from audio_spoof_detection_service.domain.entities.user import UserEntity, OneTimePasswordEntity


class SqlAlchemyUserGateway(UserGateway):
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    async def __convert_orm_to_entity(user_orm: UserOrm) -> UserEntity:
        return UserEntity(
            id=user_orm.id,
            name=user_orm.name,
            email=user_orm.email,
            refresh_token=user_orm.refresh_token,
            refresh_token_expires_at=user_orm.refresh_token_expires_at,
            registered_at=user_orm.registered_at
        )

    @staticmethod
    async def __convert_entity_to_orm(user_entity: UserEntity) -> UserOrm:
        return UserOrm(
            id=user_entity.id,
            name=user_entity.name,
            email=user_entity.email,
            refresh_token=user_entity.refresh_token,
            refresh_token_expires_at=user_entity.refresh_token_expires_at,
            registered_at=user_entity.registered_at
        )

    async def register_user(self, user: UserEntity) -> UserEntity:
        user_orm = await SqlAlchemyUserGateway.__convert_entity_to_orm(user)
        self.session.add(user_orm)
        self.session.commit()
        user.id = user_orm.id
        return user

    async def get_user_by_email(self, email: str) -> UserEntity:
        get_user_by_email_query = select(UserOrm).where(UserOrm.email == email)
        result = self.session.execute(get_user_by_email_query)
        user_orm: UserOrm = result.scalar()
        user_entity = await SqlAlchemyUserGateway.__convert_orm_to_entity(user_orm)
        return user_entity

    async def get_last_otp(self, email: str) -> OneTimePasswordEntity:
        user_orm = await self.get_user_by_email(email)
        get_last_otp_query = (
            select(OneTimePasswordOrm)
            .where(OneTimePasswordOrm.user_id == user_orm.id)
            .order_by(OneTimePasswordOrm.expires_at.desc())
            .limit(1)
        )
        result = self.session.execute(get_last_otp_query)
        otp_orm: OneTimePasswordOrm = result.scalar()
        return OneTimePasswordEntity(
            id=otp_orm.id,
            user_id=otp_orm.user_id,
            password=otp_orm.password,
            expires_at=otp_orm.expires_at,
            is_active=otp_orm.is_active
        )


    async def update_user(self, user: UserEntity) -> None:
        user_orm = await SqlAlchemyUserGateway.__convert_entity_to_orm(user)
        self.session.merge(user_orm)
        self.session.commit()

    async def is_user_exists(self, email: str) -> bool:
        is_user_exists_query = select(UserOrm).where(UserOrm.email == email)
        result = self.session.execute(is_user_exists_query)
        user_orm: UserOrm | None = result.scalar_one_or_none()
        return True if user_orm is not None else False
