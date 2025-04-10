import logging
from abc import abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

from src.api.external import ExternalService
from src.utils.dao import IRepository


logger = logging.getLogger(__name__)


TExternalEntity = TypeVar("TExternalEntity", bound=BaseModel)
TEntity = TypeVar("TEntity", bound=BaseModel)


SORT_BY = "Modified Date"


class ExternalServiceConnector(Generic[TExternalEntity, TEntity]):
    def __init__(self, external_table_name: str):
        self.external_service: ExternalService = ExternalService()

        self._external_table_name = external_table_name

    @property
    @abstractmethod
    def repository(self) -> IRepository:
        pass
