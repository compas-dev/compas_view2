import sys
import traceback
import time
from qtpy.QtCore import QObject
from qtpy.QtCore import QRunnable
from qtpy.QtCore import QThreadPool
from qtpy.QtCore import Slot
from qtpy.QtCore import Signal


class WorkerSignals(QObject):
    """Signals to allow worker to communicate with outside in event-driven manner"""

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    tick = Signal()
    progress = Signal(object)


class Worker(QRunnable):
    """Worker instance that runs in a independent thread without blocking the main process"""

    pool = QThreadPool()

    def __init__(self, fn, args=[], kwargs={}, include_self=False):
        super(Worker, self).__init__()
        self.fn = fn
        if include_self:
            args = [self] + args
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.no_signals = False

    @Slot()
    def run(self):
        """Execute the worker function, send on signals on different scenarios"""
        if self.no_signals:
            result = self.fn(*self.args, **self.kwargs)
        else:
            try:
                result = self.fn(*self.args, **self.kwargs)
            except Exception:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit((exctype, value, traceback.format_exc()))
            else:
                # Return the result of the processing
                self.signals.result.emit(result)
            finally:
                self.signals.finished.emit()  # Done


class Ticker(QRunnable):

    pool = QThreadPool()

    def __init__(self, interval=1):
        super(Ticker, self).__init__()
        self.interval = interval
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Execute the worker function, send on signals on different scenarios"""
        self.running = True
        while self.running:
            self.signals.tick.emit()
            time.sleep(self.interval)

    def stop(self):
        self.running = False
