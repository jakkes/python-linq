from __future__ import annotations
from typing import (
    Any,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    TypeVar,
    Iterable,
    Callable,
)
import collections.abc
import multiprocessing as mp
import threading as th
import queue

from linq import errors

from . import query
from .worker import Worker
from .feeder import Feeder
from .yielder import Yielder
from .task_tracker import TaskTracker


T = TypeVar("T")
S = TypeVar("S")
KT = TypeVar("KT")
VT = TypeVar("VT")


def identity(x: T) -> T:
    return x


def true(x):
    return True


class DistributedQuery(Generic[T]):
    """A query that distributes execution across multiple processes, allowing for
    utilization of multiple cores.

    Data and arguments are distributed across processes using queues from Python's
    `multiprocessing` package. This means that everything needs to be pickled, including
    functions passed to, e.g., `select`. Therefore, lambdas and local functions are not
    supported arguments to the query.
    
    ## Notes:
    1. Data and arguments are distributed across processes using queues from Python's
    `multiprocessing` package. This means that everything needs to be pickled,
    including functions passed to, e.g., `select` or `where`. Therefore, lambdas and
    local functions are not supported arguments to the query.
    2. The query may be consumed either through its execution methods, i.e. those not
    returning another `DistributedQuery` instance, or through an iterator. If
    consuming through an iterator and the iterator is not fully consumed, i.e. not
    fully looped through, then the query must be closed using its `close` method.
    Alternativly, the iteration may occur within a context manager (`with`
    statement), in which case the query is closed automatically. If unsure,
    `close` can be executed just in case. If not neceassry, it is a no-op.
        
    ## Example usage
    ```python
    >>> import time
    >>> 
    >>> def heavy_transformation(x: int):
    >>>     time.sleep(10)
    >>>     return x*2
    >>> 
    >>> def less_than_5(x: int):
    >>>     return x < 5
    >>> 
    >>> x = (
    >>>     DistributedQuery(range(100))
    >>>     .where(less_than_5)
    >>>     .select(heavy_transformation)
    >>>     .to_list()
    >>> )
    >>> assert x == [0, 1, 4, 9, 16]
    ```"""

    def __init__(
        self, sequence: Iterable[T], processes: int = None, chunk_size: int = 1
    ):
        """
        Args:
            sequence (Iterable[T]): Sequence to query.
            processes (int, optional): Number of processes to distribute the query
                across. If None, one process is spawned per CPU core. Defaults to None.
            chunk_size (int, optional): Data are distributed using this chunk size.
                Defaults to 1. By increasing the chunk size, aggregating queries may
                become more efficient, compared to a chunk size of one.
        """
        if not isinstance(sequence, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        self._sequence = sequence
        self._processes = processes if processes is not None else mp.cpu_count()
        self._chunk_size = chunk_size
        self._query = query.Executor()
        self._lock = th.Lock()

        self._feed_queue: mp.Queue = None
        self._task_queue: mp.Queue = None
        self._task_complete_queue: mp.Queue = None
        self._result_queue: mp.Queue = None
        self._feed_complete_event: th.Event = None
        self._tasks_complete_event: th.Event = None
        self._feeder: Feeder = None
        self._task_tracker: TaskTracker = None
        self._workers: List[Worker] = None

        self._executed = False
        self._closed = False

    def __iter__(self) -> Iterator[T]:
        with self._lock:
            if self._executed:
                raise AttributeError("Query has already been executed.")
            self._executed = True

        self._feed_queue = mp.Queue(maxsize=self._processes * 2)
        self._task_queue = mp.Queue()
        self._task_complete_queue = mp.Queue()
        self._result_queue = mp.Queue(maxsize=self._processes * 2)
        self._feed_complete_event = mp.Event()
        self._tasks_complete_event = mp.Event()
        self._feeder = Feeder(
            self._feed_queue,
            self._task_queue,
            self._sequence,
            self._chunk_size,
            self._feed_complete_event,
        )
        self._feeder.start()

        self._task_tracker = TaskTracker(
            self._task_queue,
            self._task_complete_queue,
            self._feed_complete_event,
            self._tasks_complete_event,
        )
        self._task_tracker.start()

        self._workers = [
            Worker(
                self._feed_queue,
                self._result_queue,
                self._feed_complete_event,
                self._tasks_complete_event,
                self._query,
            )
            for _ in range(self._processes)
        ]
        for worker in self._workers:
            worker.start()

        yield from Yielder(
            self._result_queue, self._task_complete_queue, self._tasks_complete_event
        )

        self._feeder.join()
        self._task_tracker.join()
        for worker in self._workers:
            worker.join()

    def __contains__(self, obj: T) -> bool:
        self._query.set_aggregator(query.aggregators.Contains(obj))
        return_value = False
        for x in self:
            if x:
                return_value = True
        return return_value

    def __enter__(self) -> DistributedQuery[T]:
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """Closes the query and all background threads and processes. If these have
        already been closed, this operation is a no-op."""
        if not self._executed or self._closed:
            return

        self._feed_complete_event.set()
        self._tasks_complete_event.set()
        self._task_queue.put(StopIteration)

        while not self._feed_queue.empty():
            try:
                self._feed_queue.get_nowait()
            except queue.Empty:
                pass

        while not self._result_queue.empty():
            try:
                self._result_queue.get_nowait()
            except queue.Empty:
                pass

        self._feeder.join()
        self._task_tracker.join()
        for worker in self._workers:
            worker.join()

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
        aggregator = query.aggregators.All()
        self._query.add_block(query.blocks.Select(condition))
        self._query.set_aggregator(aggregator)
        with self as self:
            return aggregator.aggregate(self)

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
        aggregator = query.aggregators.Any()
        self._query.add_block(query.blocks.Select(condition))
        self._query.set_aggregator(aggregator)
        with self as self:
            return aggregator.aggregate(self)

    def select(self, transform: Callable[[T], S]) -> DistributedQuery[S]:
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

    def where(self, condition: Callable[[T], bool]) -> DistributedQuery[T]:
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

    def argmax(self, value_fn: Callable[[T], Any]) -> T:
        """Returns the query element for which the given value function returns the
        largest value.

        Args:
            value_fn (Callable[[T], Any]): Function accepting one argument and returning
                a comparable object.

        Returns:
            T: Query element for which `value_fn` returned the largest value.
        """
        aggregator = query.aggregators.ArgMax(value_fn)
        self._query.set_aggregator(aggregator)
        return aggregator.aggregate(self)

    def argmin(self, value_fn: Callable[[T], Any]) -> T:
        """Returns the query element for which the given value function returns the
        smallest value.

        Args:
            value_fn (Callable[[T], Any]): Function accepting one argument and returning
                a comparable object.

        Returns:
            T: Query element for which `value_fn` returned the smallest value.
        """
        aggregator = query.aggregators.ArgMax(value_fn, invert_value=True)
        self._query.set_aggregator(aggregator)
        return aggregator.aggregate(self)

    def first_or_none(self, condition: Callable[[T], bool] = true) -> Optional[T]:
        """Returns the first element found to satisfy the given condition. If no element
        is found, `None` is returned.

        Note: when distributing the workload on more than one process, this function
        cannot be considered deterministic.

        Args:
            condition (Callable[[T], bool], optional): Callable accepting one argument.
                The first element for which condition returns True is returned. Defaults
                to returning `True` for any input, i.e. the result will be the first
                element encountered in the query.

        Returns:
            Optional[T]: First element encountered for which `condition` returns `True`.
                If no element is found, returns `None`.
        """
        aggregator = query.aggregators.FirstOrNone(condition)
        self._query.set_aggregator(aggregator)
        re = None
        for x in self:
            if x is None:
                continue
            if condition(x):
                re = x
                break
        self.close()
        return re

    def first(self, condition: Callable[[T], bool] = true) -> T:
        """Returns the first element found to satisfy the given condition. If no element
        is found, an exception is raised.

        Note: when distributing the workload on more than one process, this function
        cannot be considered deterministic.

        Args:
            condition (Callable[[T], bool], optional): Callable accepting one argument.
                The first element for which condition returns True is returned. Defaults
                to returning `True` for any input, i.e. the result will be the first
                element encountered in the query.

        Raises:
            errors.NoSuchElementError: In case no element is found to satisfy the
                condition.

        Returns:
            T: First element encountered for which `condition` returns `True`.
        """
        re = self.first_or_none(condition)
        if re is None:
            raise errors.NoSuchElementError()
        return re

    def last_or_none(self, condition: Callable[[T], bool] = true) -> T:
        """Returns the last element found to satisfy the given condition. If no element
        is found, `None` is returned.

        Note: when distributing the workload on more than one process, this function
        cannot be considered deterministic.

        Args:
            condition (Callable[[T], bool], optional): Callable accepting one argument.
                The last element for which condition returns True is returned. Defaults
                to returning `True` for any input, i.e. the result will be the last
                element encountered in the query.

        Returns:
            Optional[T]: Last element encountered for which `condition` returns `True`.
                If no element is found, returns `None`.
        """
        self._query.set_aggregator(query.aggregators.LastOrNone(condition))
        re = None
        for x in self:
            if x is None:
                continue
            if condition(x):
                re = x
        return re

    def last(self, condition: Callable[[T], bool] = true) -> T:
        """Returns the last element found to satisfy the given condition. If no element
        is found, an exception is raised.

        Note: when distributing the workload on more than one process, this function
        cannot be considered deterministic.

        Args:
            condition (Callable[[T], bool], optional): Callable accepting one argument.
                The last element for which condition returns True is returned. Defaults
                to returning `True` for any input, i.e. the result will be the last
                element encountered in the query.

        Raises:
            errors.NoSuchElementError: In case no element is found to satisfy the
                condition.

        Returns:
            T: Last element encountered for which `condition` returns `True`.
        """
        re = self.last_or_none(condition)
        if re is None:
            raise errors.NoSuchElementError()
        return re

    def sum(self) -> T:
        """Computes the sum over all elements. Assumes associative and commutative
        addition.

        Returns:
            T: Sum of all elements in the query.
        """
        aggregator = query.aggregators.Sum()
        self._query.set_aggregator(aggregator)
        return aggregator.aggregate(self)

    def mean(self) -> T:
        """Computes the mean of all elements. Assumes associative and commutative
        addition.

        Returns:
            T: Mean value.
        """
        self._query.set_aggregator(query.aggregators.SumAndCount())
        sum_, count = 0, 0
        for s, c in self:
            sum_ += s
            count += c
        return sum_ / count

    def to_dict(self, key: Callable[[T], KT], value: Callable[[T], VT]) -> Dict[KT, VT]:
        """Aggregates the elements found in the query into a dictionary. Keys are
        determined by the key function, and values for the value function. Note, if
        the key function does not return unique values, query elements will silently
        be lost.

        Args:
            key (Callable[[T], KT]): Callable accepting one argument, returning the
                dictionary key to be used for the particular element.
            value (Callable[[T], VT]): Callable accepting one argument, returning the
                value to be used for the given element.

        Returns:
            Dict[KT, VT]: Dictionary of `{key(x): value(x) for x in self}`.
        """
        self._query.set_aggregator(query.aggregators.Dict(key, value))
        re = {}
        for x in self:
            re.update(x)
        return re
