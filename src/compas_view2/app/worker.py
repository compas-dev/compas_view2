from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import traceback
import sys


class WorkerSignals(QObject):
    """Signals to allow worker to communicate with outside in event-driven manner
    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class Worker(QRunnable):
    """Worker instance that runs in a independent thread without blocking the main process
    """

    pool = QThreadPool()

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.no_signals = False

    @pyqtSlot()
    def run(self):
        """Execute the worker function, send on signals on different scenarios
        """
        if self.no_signals:
            result = self.fn(*self.args, **self.kwargs)
        else:
            try:
                result = self.fn(*self.args, **self.kwargs)
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit(
                    (exctype, value, traceback.format_exc()))
            else:
                # Return the result of the processing
                self.signals.result.emit(result)
            finally:
                self.signals.finished.emit()  # Done
