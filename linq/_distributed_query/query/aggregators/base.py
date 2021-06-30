from typing import Iterable, Any
import abc


class Base(abc.ABC):

    @abc.abstractmethod
    def aggregate(self, data: Iterable[Any]) -> Any:
        raise NotImplementedError
