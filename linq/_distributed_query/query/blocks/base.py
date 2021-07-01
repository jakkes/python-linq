from typing import Iterable, Iterator, Any
import abc

class Base(abc.ABC):
    
    @abc.abstractmethod
    def iterator(self, data: Iterable[Any]) -> Iterator[Any]:
        raise NotImplementedError
