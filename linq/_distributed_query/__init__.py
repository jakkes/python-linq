from typing import Any, Generic, Iterator, List, Sequence, TypeVar, Iterable, Callable
import multiprocessing as mp
import threading as th
import queue

from . import query
from .worker import Worker
from .feeder import Feeder
from .yielder import Yielder
from .task_tracker import TaskTracker


T = TypeVar("T")
S = TypeVar("S")


def identity(x: T) -> T:
    return x


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
        self._query = query.Executor()
        self._lock = th.Lock()

        self._executed = False

    def __iter__(self) -> Iterator[T]:
        with self._lock:
            if self._executed:
                raise AttributeError("Query has already been executed.")
            self._executed = True

        feed_queue = mp.Queue(maxsize=self._processes * 2)
        task_queue = mp.Queue()
        task_complete_queue = mp.Queue()
        result_queue = mp.Queue(maxsize=self._processes * 2)
        feed_complete_event = mp.Event()
        tasks_complete_event = mp.Event()
        feeder = Feeder(
            feed_queue,
            task_queue,
            self._sequence,
            self._chunk_size,
            feed_complete_event,
        )
        feeder.start()

        task_tracker = TaskTracker(
            task_queue, task_complete_queue, feed_complete_event, tasks_complete_event
        )
        task_tracker.start()

        workers = [
            Worker(feed_queue, result_queue, feed_complete_event, tasks_complete_event, self._query)
            for _ in range(self._processes)
        ]
        for worker in workers:
            worker.start()

        yield from Yielder(result_queue, task_complete_queue, tasks_complete_event)

        feeder.join()
        for worker in workers:
            worker.join()

    def __contains__(self, obj: T) -> bool:
        self._query.set_aggregator(query.aggregators.Contains(obj))
        return_value = False
        for x in self:
            if x:
                return_value = True
        return return_value

    def all(self, condition: Callable[[T], bool] = identity) -> bool:
        """Determines whether all elements in the query fulfill a given condition.

        Args:
            condition (Callable[[T], bool], optional): Callable accepting one argument
                and returning a boolean. If condition returns True for all elements in
                the query, then the function evaluates to True, otherwise False.
                Defaults to the identity function.

        Returns:
            bool: True if condition returns True for all query elements, otherwise
                False.
        """
        self._query.add_block(query.blocks.Select(condition))
        self._query.set_aggregator(query.aggregators.All())
        return_value = True
        for x in self:
            if not x:
                return_value = False
        return return_value

    def any(self, condition: Callable[[T], bool] = identity) -> bool:
        """Determines whether any element in the query fulfills a given condition.

        Args:
            condition (Callable[[T], bool], optional): Callable accepting one argument
                and returning a boolean. If condition returns True for any element
                the query, then the function evaluates to True, otherwise False.
                Defaults to the identity function.

        Returns:
            bool: True if condition evaluates to True for any query element, otherwise
                False.
        """
        self._query.add_block(query.blocks.Select(condition))
        self._query.set_aggregator(query.aggregators.Any())
        return_value = False
        for x in self:
            if x:
                return_value = True
        return return_value

    def select(self, transform: Callable[[T], S]) -> "DistributedQuery[S]":
        """Applies a transformation on each sequence element.

        Args:
            transform (Callable[[T], S]): Transform to apply.

        Returns:
            S: Return type of the transform.
        """
        self._query.add_block(query.blocks.Select(transform))
        return self

    def flatten(self) -> "DistributedQuery":
        """Flattens the query elements one step, i.e. given a list of lists,
        concatenates them into one long list.

        Returns:
            DistributedQuery: Query over flattened elements.

        Example:
        ```python
        >>> data = [[1,2,3], [4,5,6], [7, 8, 9]]
        >>> DistributedQuery(data).flatten().toList()
        [1, 2, 3, 4, 5, 6, 7, 8, 9]  # not necessarily ordered
        ```
        """
        self._query.add_block(query.blocks.Flatten())
        return self

    def to_list(self) -> List[T]:
        """Executes the query and stores the result into a list.

        Returns:
            List[T]: List of output.
        """
        return sum(self, [])

    def max(self) -> T:
        """Computes the maximum value.

        Returns:
            T: The maximum value encountered.
        """
        self._query.set_aggregator(query.aggregators.Max())
        return max(self)

    def min(self) -> T:
        """Computes the minimum value.

        Returns:
            T: Minimum value encountered.
        """
        self._query.set_aggregator(query.aggregators.Min())
        return min(self)

    def count(self) -> int:
        """Counts the number of elements in the query.

        Returns:
            int: Number of elements matching the query.
        """
        self._query.set_aggregator(query.aggregators.Count())
        return sum(self)

    def where(self, condition: Callable[[T], bool]) -> "DistributedQuery[T]":
        """Filters the query on a given condition.

        Args:
            condition (Callable[[T], bool]): Condition accepting one argument and
                returning a boolean. Elements for which the condition evaluates to True
                are kept.

        Returns:
            DistributedQuery[T]: Query where elements pass the condition.
        """
        self._query.add_block(query.blocks.Where(condition))
        return self

    def contains(self, obj: T) -> bool:
        """Determines whether the given object is found in the query.

        Args:
            obj (T): Object to search for.

        Returns:
            bool: True if the object was found, otherwise False.
        """
        return obj in self

    def argmax(self, value: Callable[[T], Any]) -> T:
        pass
