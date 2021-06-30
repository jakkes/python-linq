from typing import Any, Generic, Iterator, Sequence, TypeVar, Iterable, Callable, List
import abc
import multiprocessing as mp
import threading as th
import queue
import time


T = TypeVar("T")
S = TypeVar("S")


class _Worker(mp.Process):
    def __init__(
        self,
        feed_queue: mp.JoinableQueue,
        result_queue: mp.JoinableQueue,
        feed_complete_event: th.Event,
        query: "_Query",
    ):
        super().__init__(daemon=True)
        self._feed_queue = feed_queue
        self._result_queue = result_queue
        self._feed_complete_event = feed_complete_event
        self._query = query

    def run(self):
        while not self._feed_complete_event.is_set() or not self._feed_queue.empty():
            try:
                data: Sequence[Any] = self._feed_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue
            self._result_queue.put(list(self._query.execute(data)))
            self._feed_queue.task_done()


class _Query:
    def __init__(self):
        self._blocks: "List[_QueryBlock]" = []

    def add_block(self, block: "_QueryBlock"):
        self._blocks.append(block)

    def execute(self, data: Sequence[Any]) -> Iterator[Any]:
        if len(self._blocks) == 0:
            yield from data
            return

        iterator = self._blocks[0].iterator(data)
        for i in range(1, len(self._blocks)):
            iterator = self._blocks[i].iterator(iterator)
        yield from iterator


class _QueryBlock(abc.ABC):
    
    @abc.abstractmethod
    def iterator(self, data: Iterable[Any]) -> Iterator[Any]:
        raise NotImplementedError


class _WhereBlock(_QueryBlock):
    def __init__(self, condition: Callable[[Any], bool]) -> None:
        super().__init__()
        self._condition = condition

    def iterator(self, data: Iterable[Any]) -> Iterator[Any]:
        for x in data:
            if self._condition(x):
                yield x


class _SelectBlock(_QueryBlock):
    def __init__(self, transform: Callable[[Any], Any]) -> None:
        super().__init__()
        self._transform = transform

    def iterator(self, data: Iterable[Any]) -> Iterator[Any]:
        for x in data:
            yield self._transform(x)


class DistributedQuery(Generic[T]):
    """A query that distributes execution across multiple processes, allowing for
    utilization of multiple cores.
    
    Data and arguments are distributed across processes using queues from Python's
    `multiprocessing` package. This means that everything needs to be pickled, including
    functions passed to, e.g., `select`. Therefore, lambdas and local functions are not
    supported arguments to the query."""

    def __init__(
        self, sequence: Iterable[T], processes: int = None, chunk_size: int = 1
    ):
        """
        Args:
            sequence (Iterable[T]): Sequence to query.
            processes (int, optional): Number of processes to distribute the query
                across. If None, one process is spawned per CPU core. Defaults to None.
            chunk_size (int, optional): Data are distributed using this chunk size.
                Defaults to 1.
        """
        self._sequence = sequence
        self._processes = processes if processes is not None else mp.cpu_count()
        self._chunk_size = chunk_size
        self._query = _Query()
        self._lock = th.Lock()

        self._executed = False

    def _feeder(self, feed_queue: mp.JoinableQueue, complete_event: th.Event):
        chunk = []
        for data in self._sequence:
            chunk.append(data)
            if len(chunk) >= self._chunk_size:
                feed_queue.put(chunk.copy())
                chunk.clear()
        if len(chunk) > 0:
            feed_queue.put(chunk)
        complete_event.set()

    def _feeder_tasks_done(self, queue: mp.JoinableQueue, event: th.Event):
        queue.join()
        event.set()

    def __iter__(self) -> Iterator[T]:
        with self._lock:
            if self._executed:
                raise AttributeError("Query has already been executed.")
            self._executed = True

        feed_queue = mp.JoinableQueue(maxsize=self._processes * 2)
        feed_complete_event = mp.Event()
        feeder_thread = th.Thread(
            target=self._feeder, args=(feed_queue, feed_complete_event)
        )
        feeder_thread.start()

        result_queue = mp.JoinableQueue(maxsize=self._processes * 2)

        workers = [
            _Worker(feed_queue, result_queue, feed_complete_event, self._query)
            for _ in range(self._processes)
        ]
        for worker in workers:
            worker.start()

        while not feed_complete_event.is_set():
            try:
                data = result_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue
            yield from data
        feeder_thread.join()

        feeder_tasks_done = th.Event()
        feeder_tasks_done_thread = th.Thread(
            target=self._feeder_tasks_done, args=(feed_queue, feeder_tasks_done)
        )
        feeder_tasks_done_thread.start()

        while not feeder_tasks_done.is_set() or not result_queue.empty():
            try:
                data = result_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue
            yield from data

        for worker in workers:
            worker.join()

    def __contains__(self, obj: T) -> bool:
        for x in self:
            if obj == x:
                return True
        return False

    def select(self, transform: Callable[[T], S]) -> "DistributedQuery[S]":
        """Applies a transformation on each sequence element.

        Args:
            transform (Callable[[T], S]): Transform to apply.

        Returns:
            S: Return type of the transform.
        """
        self._query.add_block(_SelectBlock(transform))
        return self

    def max(self) -> T:
        """Computes the maximum value.

        Returns:
            T: The maximum value encountered.
        """
        return max(self)

    def min(self) -> T:
        """Computes the minimum value.

        Returns:
            T: Minimum value encountered.
        """
        return min(self)

    def count(self) -> int:
        """Counts the number of elements in the query.

        Returns:
            int: Number of elements matching the query.
        """
        return sum(1 for _ in self)

    def where(self, condition: Callable[[T], bool]) -> "DistributedQuery[T]":
        self._query.add_block(_WhereBlock(condition))
        return self

    def contains(self, obj: T) -> bool:
        """Determines whether the given object is found in the query.

        Args:
            obj (T): Object to search for.

        Returns:
            bool: True if the object was found, otherwise False.
        """
        return obj in self    
