from typing import List, Sequence, Any, Iterator
from . import blocks

class Executor:
    def __init__(self):
        self._blocks: List[blocks.Base] = []

    def add_block(self, block: blocks.Base):
        self._blocks.append(block)

    def execute(self, data: Sequence[Any]) -> Iterator[Any]:
        if len(self._blocks) == 0:
            yield from data
            return

        iterator = self._blocks[0].iterator(data)
        for i in range(1, len(self._blocks)):
            iterator = self._blocks[i].iterator(iterator)
        yield from iterator
