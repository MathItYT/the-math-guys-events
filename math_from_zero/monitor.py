from pathlib import Path
from subprocess import run
import time

from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from watchdog.observers.api import (
    BaseObserver, 
    EventQueue,
    DEFAULT_OBSERVER_TIMEOUT,
    DEFAULT_EMITTER_TIMEOUT
)
from watchdog.observers.read_directory_changes import WindowsApiEmitter


class Emitter(WindowsApiEmitter):
    def __init__(self, event_queue: EventQueue, watch, timeout=DEFAULT_EMITTER_TIMEOUT):
        super().__init__(event_queue, watch, timeout)

    def on_thread_start(self):
        if self.is_alive():
            self.stop()
            self.join()
        super().on_thread_start()


class Observer(BaseObserver):
    def __init__(self, timeout: int = DEFAULT_OBSERVER_TIMEOUT):
        super().__init__(emitter_class=Emitter, timeout=timeout)


class EventHandler(FileSystemEventHandler):
    def on_modified(self, event: FileModifiedEvent):
        if Path(event.src_path).name not in ("template.tex", "template.html"):
            return
        print("Modified, running make again...")
        run(["python", "main.py"], stdout=None)


class Monitor:
    def __init__(self, path: str):
        self.path = path
        self.observer = Observer()
        self.event_handler = EventHandler()

    def run(self):
        self.observer.schedule(
            self.event_handler,
            self.path,
            recursive=False
        )
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()


if __name__ == "__main__":
    while True:
        print("Monitoring template.tex and template.html for changes...")
        try:
            m = Monitor(".")
            m.run()
            while True:
                time.sleep(1.0)
        except KeyboardInterrupt:
            m.stop()
            print("Stopped monitoring")
            break
