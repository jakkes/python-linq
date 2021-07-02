import queue
import multiprocessing as mp
import threading as th


class TaskTracker(th.Thread):
    def __init__(
        self,
        task_queue: mp.Queue,
        complete_queue: mp.Queue,
        task_event: th.Event,
        complete_event: th.Event,
    ):
        super().__init__(daemon=True, name="TaskTrackerThread")
        self._complete_queue = complete_queue
        self._complete_event = complete_event
        self._task_queue = task_queue
        self._task_event = task_event

    def run(self) -> None:
        tasks = 0
        while True:
            try:
                data = self._task_queue.get(timeout=0.1)
                if data is StopIteration:
                    break
                tasks += data
            except queue.Empty:
                continue

        while tasks > 0 and not self._complete_event.is_set():
            try:
                self._complete_queue.get(timeout=0.1)
            except queue.Empty:
                continue
            tasks -= 1
        self._complete_event.set()
