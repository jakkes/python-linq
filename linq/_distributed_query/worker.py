from typing import Sequence, Any
import multiprocessing as mp
import threading as th
from . import query


class Worker(mp.Process):
    def __init__(
        self,
        feed_queue: mp.JoinableQueue,
        result_queue: mp.JoinableQueue,
        feed_complete_event: th.Event,
        query: query.Executor,
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