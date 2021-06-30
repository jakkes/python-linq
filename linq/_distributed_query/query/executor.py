from typing import Callable, List, Sequence, Any, Iterator, TypeVar
from . import blocks, aggregators


T = TypeVar("T")


class Executor:
    def __init__(self):
        self._blocks: List[blocks.Base] = []
        self._aggregator: aggregators.Base = aggregators.List()

    def add_block(self, block: blocks.Base):
        self._blocks.append(block)

    def set_aggregator(self, aggregator: aggregators.Base):
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
        return self._aggregator.aggregate(self._iterator(data))
