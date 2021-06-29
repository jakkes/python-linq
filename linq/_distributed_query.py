from typing import Any, Generic, Iterator, Sequence, TypeVar, Iterable, Callable
import multiprocessing as mp
import threading as th
import queue


T = TypeVar("T")
S = TypeVar("S")


class _Worker(mp.Process):
    def __init__(
        self,
        feed_queue: mp.JoinableQueue,
        result_queue: mp.JoinableQueue,
        feed_complete_event: th.Event,
        operations,
    ):
        super().__init__(daemon=True)
        self.__feed_queue = feed_queue
        self.__result_queue = result_queue
        self.__feed_complete_event = feed_complete_event
        self.__operations = operations

    def __execute(self, data: Any) -> Any:
        for op in self.__operations:
            data = op(data)
        return data

    def run(self):
        while not self.__feed_complete_event.is_set() or not self.__feed_queue.empty():
            try:
                data: Sequence[Any] = self.__feed_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue
            self.__result_queue.put([self.__execute(x) for x in data])
            self.__feed_queue.task_done()


class DistributedQuery(Generic[T]):
    """A query that distributes execution across multiple processes, allowing for
    utilization of multiple cores."""

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
        self.__sequence = sequence
        self.__processes = processes if processes is not None else mp.cpu_count()
        self.__chunk_size = chunk_size
        self.__operations = []
        self.__lock = th.Lock()

        self.__executed = False

    def __feeder(self, feed_queue: mp.JoinableQueue, complete_event: th.Event):
        chunk = []
        for data in self.__sequence:
            chunk.append(data)
            if len(chunk) >= self.__chunk_size:
                feed_queue.put(chunk.copy())
                chunk.clear()
        if len(chunk) > 0:
            feed_queue.put(chunk)
        complete_event.set()

    def __feeder_tasks_done(self, queue: mp.JoinableQueue, event: th.Event):
        queue.join()
        event.set()

    def __iter__(self) -> Iterator[T]:
        with self.__lock:
            if self.__executed:
                raise AttributeError("Query has already been executed.")
            self.__executed = True

        feed_queue = mp.JoinableQueue(maxsize=self.__processes * 2)
        feed_complete_event = mp.Event()
        feeder_thread = th.Thread(
            target=self.__feeder, args=(feed_queue, feed_complete_event)
        )
        feeder_thread.start()

        result_queue = mp.JoinableQueue(maxsize=self.__processes * 2)

        workers = [
            _Worker(feed_queue, result_queue, feed_complete_event, self.__operations)
            for _ in range(self.__processes)
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
            target=self.__feeder_tasks_done, args=(feed_queue, feeder_tasks_done)
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

    def select(self, transform: Callable[[T], S]) -> "DistributedQuery[S]":
        """Applies a transformation on each sequence element.

        Args:
            transform (Callable[[T], S]): Transform to apply.

        Returns:
            S: Return type of the transform.
        """
        self.__operations.append(transform)
        return self

    def max(self) -> T:
        return max(self)
