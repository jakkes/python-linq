import multiprocessing as mp
import threading as th
from typing import Any, Sequence


class Feeder(th.Thread):
    def __init__(
        self,
        feed_queue: mp.JoinableQueue,
        data: Sequence[Any],
        chunk_size: int,
        all_data_fed_event: th.Event,
        all_tasks_complete_event: th.Event,
    ):
        super().__init__()

        self._feed_queue = feed_queue
        self._data = data
        self._chunk_size = chunk_size
        self._data_fed_event = all_data_fed_event
        self._tasks_complete_event = all_tasks_complete_event

    def run(self) -> None:
        chunk = []
        for data in self._data:
            chunk.append(data)
            if len(chunk) >= self._chunk_size:
                self._feed_queue.put(chunk.copy())
                chunk.clear()
        if len(chunk) > 0:
            self._feed_queue.put(chunk)
        self._data_fed_event.set()
        self._feed_queue.join()
        self._tasks_complete_event.set()
