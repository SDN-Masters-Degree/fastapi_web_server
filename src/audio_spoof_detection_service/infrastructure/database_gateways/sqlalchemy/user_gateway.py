from sqlalchemy import select
from sqlalchemy.orm import Session

from audio_spoof_detection_service.application.protocols.database_gateways.user_gateway import UserGateway
from audio_spoof_detection_service.infrastructure.database_gateways.sqlalchemy.orm import UserOrm
from audio_spoof_detection_service.domain.entities.user import UserEntity


class SqlAlchemyUserGateway(UserGateway):
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    async def __convert_orm_to_entity(user_orm: UserOrm) -> UserEntity:
        return UserEntity(
            id=user_orm.id,
            name=user_orm.name,
            email=user_orm.email,
            hashed_password=user_orm.hashed_password,
            refresh_token=user_orm.refresh_token,
            registered_at=user_orm.registered_at
        )

    @staticmethod
    async def __convert_entity_to_orm(user_entity: UserEntity) -> UserOrm:
        return UserOrm(
            id=user_entity.id,
            name=user_entity.name,
            email=user_entity.email,
            hashed_password=user_entity.hashed_password,
            refresh_token=user_entity.refresh_token,
            registered_at=user_entity.registered_at
        )

    async def register_user(self, user: UserEntity) -> UserEntity:
        user_orm = await SqlAlchemyUserGateway.__convert_entity_to_orm(user)
        self.session.add(user_orm)
        self.session.commit()
        user.id = user_orm.id
        return user

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        get_user_by_email_query = select(UserOrm).where(UserOrm.email == email)
        result = self.session.execute(get_user_by_email_query)
        user_orm: UserOrm = result.scalar()

        if user_orm is None:
            return None

        user_entity = await SqlAlchemyUserGateway.__convert_orm_to_entity(user_orm)
        return user_entity

    async def get_user_by_refresh_token(self, refresh_token: str) -> UserEntity | None:
        get_user_by_refresh_token_query = select(UserOrm).where(UserOrm.refresh_token == refresh_token)
        result = self.session.execute(get_user_by_refresh_token_query)
        user_orm: UserOrm = result.scalar()

        if user_orm is None:
            return None

        user_entity = await SqlAlchemyUserGateway.__convert_orm_to_entity(user_orm)
        return user_entity

    async def update_user(self, user: UserEntity) -> None:
        user_orm = await SqlAlchemyUserGateway.__convert_entity_to_orm(user)
        self.session.merge(user_orm)
        self.session.commit()

    async def is_user_exists(self, email: str) -> bool:
        is_user_exists_query = select(UserOrm).where(UserOrm.email == email)
        result = self.session.execute(is_user_exists_query)
        user_orm: UserOrm | None = result.scalar_one_or_none()
        return True if user_orm is not None else False
