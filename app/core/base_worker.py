import queue
import threading
import uuid

import loguru


class BaseWorker:
    def __init__(self):
        self.queue = queue.Queue()
        self.background_close_signal = threading.Event()
        self.init()

    def init(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def sync_start(self):
        raise NotImplementedError

    async def async_start(self):
        async for model in self.run():
            model.id = uuid.uuid4()
            self.queue.put(model, block=False)
            if self.background_close_signal.is_set():
                raise Exception("Background task has been closed")

    def start(self):
        threading.Thread(target=self.start_background_task, daemon=True).start()
        self.start_main_task()


