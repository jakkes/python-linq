import multiprocessing as mp
import threading as th
from typing import Any, Iterable


class Feeder(th.Thread):
    def __init__(
        self,
        feed_queue: mp.Queue,
        task_queue: mp.Queue,
        data: Iterable[Any],
        chunk_size: int,
        all_data_fed_event: th.Event,
    ):
        super().__init__(daemon=True, name="FeederThread")

        self._feed_queue = feed_queue
        self._task_queue = task_queue
        self._data = data
        self._chunk_size = chunk_size
        self._data_fed_event = all_data_fed_event

    def run(self) -> None:
        chunk = []

        for data in self._data:
            if self._data_fed_event.is_set():
                return

            chunk.append(data)
            if len(chunk) >= self._chunk_size:
                self._feed_queue.put(chunk.copy())
                self._task_queue.put(1)
                chunk.clear()
        if len(chunk) > 0:
            self._feed_queue.put(chunk)
            self._task_queue.put(1)
        self._task_queue.put(StopIteration)
        self._data_fed_event.set()
