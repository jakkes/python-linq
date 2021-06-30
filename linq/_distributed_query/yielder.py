import queue
import threading as th
import multiprocessing as mp
from typing import Any, Iterator

class Yielder:
    def __init__(self, result_queue: mp.Queue, all_tasks_done_event: th.Event):
        self._result_queue = result_queue
        self._tasks_done_event = all_tasks_done_event

    def __iter__(self) -> Iterator[Any]:
        while not self._tasks_done_event.is_set() or not self._result_queue.empty():
            try:
                data = self._result_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue
            yield from data
