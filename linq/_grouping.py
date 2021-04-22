from typing import Generic, TypeVar, Sequence, List

KT = TypeVar("KT")
VT = TypeVar("VT")


class Grouping(Generic[KT, VT]):
    """Sequence of values grouped under one key. This object is initialized by some
    query methods."""

    def __init__(self, key: KT, values: Sequence[VT]):
        """
        Args:
            key (KT): Key.
            values (Sequence[VT]): Sequence of values associated to `key`.
        """
        self._values = list(values)
        self._key = key

    @property
    def values(self) -> List[VT]:
        """Values."""
        return self._values

    @property
    def key(self) -> KT:
        """Key."""
        return self._key

    def __iter__(self):
        yield from self._values

    def __repr__(self):
        return {
            self._key: self._values
        }.__repr__()
