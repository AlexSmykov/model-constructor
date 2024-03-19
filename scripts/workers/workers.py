import time

from PyQt5.QtCore import *

from scripts.model import fit, predict
from .worker_signals import WorkerSignals


class Fitter(QRunnable):
    def __init__(self, model, optimizer, epochs, layers: dict[str: dict[str: float]], dataset_size, images_shape):
        self.model = model
        self.optimizer = optimizer
        self.epochs = epochs
        self.layers = layers
        self.dataset_size = dataset_size
        self.images_shape = images_shape

        super(Fitter, self).__init__()
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.signals.start.emit(self)
        time.sleep(0.1)
        results = fit(self.model, self.optimizer, self.epochs, self.layers, self.dataset_size, self.images_shape)
        self.signals.end.emit(results)

    def write(self, text):
        text += ''
        if text == '' or text == '\n' or text is None or 'Found' in text:
            return

        text = text[:-1] if text[-1] == '\n' else text
        text = text.replace('\n', '')
        text = text.replace('', '')
        self.signals.output.emit(text)

    def flush(self):
        ...


class Predictor(QRunnable):
    def __init__(self, model, batch_size, images_shape):
        self.model = model
        self.batch_size = batch_size
        self.images_shape = images_shape

        super(Predictor, self).__init__()
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.signals.start.emit(self)
        time.sleep(0.1)
        results = predict(self.model, self.batch_size, self.images_shape)
        self.signals.end.emit(results)

    def write(self, text):
        text += ''
        if text == '' or text == '\n' or text is None or 'Found' in text:
            return

        text = text[:-1] if text[-1] == '\n' else text
        text = text.replace('\n', '')
        text = text.replace('', '')
        self.signals.output.emit(text)

    def flush(self):
        ...
