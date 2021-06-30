from typing import Callable, Any, Iterator, Iterable
from .base import Base

class Where(Base):
    def __init__(self, condition: Callable[[Any], bool]) -> None:
        super().__init__()
        self._condition = condition

    def iterator(self, data: Iterable[Any]) -> Iterator[Any]:
        for x in data:
            if self._condition(x):
                yield x
