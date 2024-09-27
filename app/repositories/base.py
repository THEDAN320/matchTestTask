from abc import abstractmethod
from typing import Protocol, Dict, Any, runtime_checkable

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from app.configs.database import database_session


@runtime_checkable
class AbstractRepository(Protocol):
    model: Any

    @abstractmethod
    def add(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError


class Repository(AbstractRepository):
    def add(self, data: Dict[str, Any]) -> None:
        with database_session.begin() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            try:
                result = session.execute(stmt)
                session.commit()
                return result.scalar_one()
            except IntegrityError:
                session.rollback()
