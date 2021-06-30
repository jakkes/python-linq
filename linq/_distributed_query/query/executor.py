from typing import Callable, List, Sequence, Any, Iterator, TypeVar
from . import blocks


T = TypeVar("T")


class Executor:
    def __init__(self):
        self._blocks: List[blocks.Base] = []
        self._aggregator: Callable[[Iterator], Any] = list

    def add_block(self, block: blocks.Base):
        self._blocks.append(block)

    def set_aggregator(self, aggregator: Callable[[Iterator], Any]):
        self._aggregator = aggregator

    def _iterator(self, data: Sequence[T]) -> Iterator[T]:
        if len(self._blocks) == 0:
            yield from data
            return

        iterator = self._blocks[0].iterator(data)
        for i in range(1, len(self._blocks)):
            iterator = self._blocks[i].iterator(iterator)
        yield from iterator

    def execute(self, data: Sequence[T]) -> Any:
        return self._aggregator(self._iterator(data))
