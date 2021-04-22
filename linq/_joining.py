from typing import Generic, TypeVar, Iterable, List

T = TypeVar("T")
S = TypeVar("S")


class Joining(Generic[T, S]):

    def __init__(self, inner: T, outer: Iterable[S]):
        self._inner = inner
        self._outer = outer

    @property
    def inner(self) -> T:
        return self._inner

    @property
    def outer(self) -> List[S]:
        return self._outer

    def __iter__(self):
        yield from self._outer

    def __repr__(self):
        return {
            "inner": self._inner,
            "outer": self._outer
        }.__repr__()
