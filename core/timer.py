import time
class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""
class Timer:
    def __init__(self):
        self._start_time = None
        self._paused_time = None

    def start(self):
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def pause(self):
        if self._paused_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._paused_time = time.perf_counter()

    def unpause(self):
        if self._paused_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._paused_time
        self._paused_time = None
        self._start_time = self._start_time + elapsed_time

    def stop(self):
        if self._start_time is not None:
            elapsed_time = time.perf_counter() - self._start_time
            self._start_time = None
            print(f"Elapsed time: {elapsed_time:0.4f} seconds")
            return elapsed_time
