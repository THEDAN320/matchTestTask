from abc import abstractmethod
from typing import Protocol, Dict, Any, runtime_checkable
from uuid import UUID

from sqlalchemy import insert, update, select
from sqlalchemy.exc import IntegrityError, DataError

from app.configs.database import database_session


@runtime_checkable
class AbstractRepository(Protocol):
    model: Any

    @abstractmethod
    def add(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, uuid: UUID, data: Dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, filter_by: dict) -> list[dict[str, Any]]:
        raise NotImplementedError


class Repository(AbstractRepository):
    def add(self, data: Dict[str, Any]) -> None:
        with database_session.begin() as session:
            stmt = insert(self.model).values(**data)
            try:
                session.execute(stmt)
                session.commit()
            except IntegrityError:
                session.rollback()
            except DataError:
                session.rollback()

    def update(self, uuid: UUID, data: Dict[str, Any]) -> None:
        with database_session.begin() as session:
            stmt = update(self.model).where(self.model.uuid == uuid).values(**data)
            try:
                session.execute(stmt)
                session.commit()
            except IntegrityError:
                session.rollback()
            except DataError:
                session.rollback()

    def get_all(self, filter_by: dict) -> list[dict[str, Any]]:
        with database_session.begin() as session:
            results = (
                session.execute(
                    select(self.model).filter_by(**filter_by)
                )
                .scalars()
                .all()
            )
            return (result for result in results)
