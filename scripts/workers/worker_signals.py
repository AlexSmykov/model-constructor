from PyQt5.QtCore import QObject, pyqtSignal


class WorkerSignals(QObject):
    start = pyqtSignal(object)
    output = pyqtSignal(str)
    end = pyqtSignal(tuple)
