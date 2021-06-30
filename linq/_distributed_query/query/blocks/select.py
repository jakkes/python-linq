from typing import Callable, Any, Iterator, Iterable
from .base import Base


class Select(Base):
    def __init__(self, transform: Callable[[Any], Any]) -> None:
        super().__init__()
        self._transform = transform

    def iterator(self, data: Iterable[Any]) -> Iterator[Any]:
        for x in data:
            yield self._transform(x)
