import queue
import threading as th
import multiprocessing as mp
from typing import Any, Iterator

class Yielder:
    def __init__(self, result_queue: mp.Queue, task_complete_queue: mp.Queue, all_tasks_done_event: th.Event):
        self._result_queue = result_queue
        self._tasks_done_event = all_tasks_done_event
        self._task_complete_queue = task_complete_queue

    def __iter__(self) -> Iterator[Any]:
        while not self._tasks_done_event.is_set():
            try:
                data = self._result_queue.get(block=True, timeout=0.1)
            except queue.Empty:
                continue
            self._task_complete_queue.put(1)
            yield data
