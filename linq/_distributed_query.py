from typing import Generic, Iterator, TypeVar, Iterable
import multiprocessing as mp
import threading as th


T = TypeVar("T")


class _Worker(mp.Process):
    def __init__(self, data_queue: mp.Queue, result_queue: mp.Queue, operations):
        super().__init__(daemon=True)
        self._data_queue = data_queue
        self._result_queue = result_queue
        self._operatoins = operations

    def run(self):
        pass

class DistributedQuery(Generic[T]):
    """A query that distributes execution across multiple processes, allowing for
    utilization of multiple cores."""
    
    def __init__(self, sequence: Iterable[T], processes: int = None, chunk_size: int=1):
        """
        Args:
            sequence (Iterable[T]): Sequence to query.
            processes (int, optional): Number of processes to distribute the query
                across. If None, one process is spawned per CPU core. Defaults to None.
            chunk_size (int, optional): Data are distributed using this chunk size.
                Defaults to 1.
        """
        self.__sequence = sequence
        self.__processes = processes
        self.__chunk_size = chunk_size
        self.__lock = th.Lock()

        self.__executed = False

    def __iter__(self) -> Iterator[T]:
        with self.__lock:
            if self.__executed:
                raise AttributeError("Query has already been executed.")
            self.__executed = True

        raise NotImplementedError
