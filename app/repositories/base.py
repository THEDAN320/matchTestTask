from abc import abstractmethod
from collections.abc import Generator
from typing import Any, Protocol, runtime_checkable
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.exc import DataError, IntegrityError

from app.configs.database import database_session


@runtime_checkable
class AbstractRepository(Protocol):
    model: Any

    @abstractmethod
    def add(self, data: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, uuid: UUID, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, filter_by: dict) -> Generator[dict[str, Any], None, None]:
        raise NotImplementedError

    @abstractmethod
    def get_range(
        self, offset: int = 0, count: int = 1000
    ) -> Generator[dict[str, Any], None, None]:
        raise NotImplementedError


class Repository(AbstractRepository):
    def add(self, data: dict[str, Any]) -> None:
        with database_session.begin() as session:
            stmt = insert(self.model).values(**data)
            try:
                session.execute(stmt)
                session.commit()
            except IntegrityError:
                session.rollback()
            except DataError:
                session.rollback()

    def update(self, uuid: UUID, data: dict[str, Any]) -> None:
        with database_session.begin() as session:
            stmt = update(self.model).where(self.model.uuid == uuid).values(**data)
            try:
                session.execute(stmt)
                session.commit()
            except IntegrityError:
                session.rollback()
            except DataError:
                session.rollback()

    def get_all(self, filter_by: dict) -> Generator[dict[str, Any], None, None]:
        with database_session.begin() as session:
            results = (
                session.execute(select(self.model).filter_by(**filter_by))
                .scalars()
                .all()
            )
            return (result.read() for result in results)

    def get_range(
        self, offset: int = 0, count: int = 1000
    ) -> Generator[dict[str, Any], None, None]:
        with database_session.begin() as session:
            results = (
                session.execute(select(self.model).limit(count).offset(offset))
                .scalars()
                .all()
            )
            return (result.read() for result in results)
