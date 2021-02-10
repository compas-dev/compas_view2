from PySide2 import QtCore


class Timer:

    def __init__(self, interval, callback, singleshot=False):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(callback)
        self.timer.setSingleShot(singleshot)
        self.timer.start()
