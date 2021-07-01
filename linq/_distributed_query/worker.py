from typing import Sequence, Any
import queue
import multiprocessing as mp
import threading as th
from . import query


class Worker(mp.Process):
    def __init__(
        self,
        feed_queue: mp.Queue,
        result_queue: mp.Queue,
        feed_complete_event: th.Event,
        task_complete_event: th.Event,
        query: query.Executor,
    ):
        super().__init__(daemon=True)
        self._feed_queue = feed_queue
        self._result_queue = result_queue
        self._feed_complete_event = feed_complete_event
        self._task_complete_event = task_complete_event
        self._query = query

    def run(self):
        while not (self._feed_complete_event.is_set() and self._task_complete_event.is_set()):
            try:
                data: Sequence[Any] = self._feed_queue.get(block=True, timeout=0.1)
            except queue.Empty:
                continue
            self._result_queue.put(self._query.execute(data))
