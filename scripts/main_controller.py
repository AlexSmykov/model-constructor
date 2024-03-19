import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scripts.enums.layers_enum import ELayers
from scripts.enums.optimizers_enum import EOptimizers
from scripts.model import clear
from scripts.uis.layer_select_dialog.layer_select_controller import LayerSelectController
from scripts.uis.layer_widget.layer_controller import LayerController
from scripts.uis.main_window.ui import Ui_MainWindow
from scripts.utils.flatten_array_of_dicts import flatten_array_of_dicts
from scripts.workers.workers import Fitter, Predictor


class MainController(Ui_MainWindow):
    model_layers: list[LayerController] = []

    def __init__(self):
        self.nn_model = None
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.app = QApplication(sys.argv)
        self.GenerateWindow = QMainWindow()
        self.setupUi(self.GenerateWindow)

        self.on_start()

        self.GenerateWindow.show()
        sys.exit(self.app.exec_())

    def set_signals_connection(self):
        self.fitting_button.clicked.connect(self.fit)
        self.predict_button.clicked.connect(self.predict)
        self.exit_button.clicked.connect(self.on_exit)
        self.delete_model_button.clicked.connect(self.clear_model)
        self.change_model_button.clicked.connect(self.change_model)
        self.save_model_button.clicked.connect(self.save_model)
        self.add_layer_button.clicked.connect(self.open_layer_select_modal)

    # region App lifecycle
    def on_start(self):
        self.set_signals_connection()
        self.delete_model_button.setEnabled(False)
        self.save_model_button.setEnabled(False)
        self.add_layer_button.setEnabled(False)
        self.predict_button.setEnabled(False)

        # Buttons

        self.update_prediction_image()
        self.update_optimizers()

        self.prediction_log.clear()
        self.fitting_log.clear()

    def on_exit(self):
        QCoreApplication.instance().quit()

    # endregion

    # region Model
    def clear_model(self):
        self.predict_results.setText('')
        self.fit_before_prediction_label.setText('Fit before prediction!')
        self.fitting_button.setEnabled(True)
        self.delete_model_button.setEnabled(False)
        self.optimizer_combo_box.setEnabled(True)
        self.train_dataset_size_spin_box.setEnabled(True)
        self.optimizer_combo_box.setEnabled(True)
        self.train_dataset_size_spin_box.setEnabled(True)
        self.set_model_prediction_active(False)

        self.update_prediction_image()
        self.update_prediction_correct_image()

        self.nn_model = None
        clear()

    def change_model(self):
        self.change_model_button.setEnabled(False)
        self.save_model_button.setEnabled(True)
        self.add_layer_button.setEnabled(True)

    def save_model(self):
        self.change_model_button.setEnabled(True)
        self.save_model_button.setEnabled(False)
        self.add_layer_button.setEnabled(False)

        self.clear_model()

    # endregion

    # region Threading (fitting / prediction)
    def fit(self):
        image_scale = self.image_scale_spin_box.value()
        worker = Fitter(self.nn_model,
                        self.optimizer_combo_box.currentText(),
                        self.epoch_count_spin_box.value(),
                        self.get_layers_data(),
                        self.train_dataset_size_spin_box.value(),
                        (int(image_scale), int(image_scale)))

        worker.signals.start.connect(self.on_start_fitting)
        worker.signals.output.connect(self.update_fitting_log)
        worker.signals.end.connect(self.on_end_fitting)

        self.threadpool.start(worker)

    def on_start_fitting(self, stream: QRunnable):
        self.set_model_constructor_active(False)

        self.predict_button.setEnabled(False)

        set_output_stream(stream)

    def on_end_fitting(self, results):
        self.set_model_constructor_active(True)

        reset_output()

        if len(results) <= 0:
            reset_output()
            return

        self.set_model_prediction_active(True)
        self.fit_before_prediction_label.setText('')
        self.nn_model = results[0]

    def predict(self):
        image_scale = self.image_scale_spin_box.value()
        worker = Predictor(self.nn_model, self.prediction_batch_size_spin_box.value(),
                           (int(image_scale), int(image_scale)))

        worker.signals.start.connect(self.on_start_predict)
        worker.signals.output.connect(self.update_prediction_log)
        worker.signals.end.connect(self.on_end_predict)

        self.threadpool.start(worker)

    def on_start_predict(self, stream: QRunnable):
        self.set_model_constructor_active(False)
        self.set_model_prediction_active(False)

        set_output_stream(stream)

    def on_end_predict(self, results):
        self.update_prediction_image(False, 1 / (256 / self.image_scale_spin_box.value()))
        self.predict_results.setText(f'Cat: {results[0][results[3]][0]:.5f} | Dog: {results[0][results[3]][1]:.5f}')
        is_correct = results[0][results[3]][results[2][results[3]]] > 0.5
        self.update_prediction_correct_image(is_correct)

        for result in results[0]:
            if result[results[2][results[3]]] > 0.5:
                self.prediction_log.appendPlainText("Correct prediction")
            else:
                self.prediction_log.appendPlainText("Incorrect prediction")

        self.set_model_constructor_active(True)
        self.set_model_prediction_active(True)

        reset_output()

    # endregion

    # region Set active (some)
    def set_model_constructor_active(self, active: bool):
        self.train_dataset_size_spin_box.setEnabled(active)
        self.save_model_button.setEnabled(active)
        self.change_model_button.setEnabled(active)
        self.optimizer_combo_box.setEnabled(active)
        self.delete_model_button.setEnabled(active)
        self.fitting_button.setEnabled(active)

        map(lambda layer: layer.enable() if active else layer.disable(), self.model_layers)

    def set_model_prediction_active(self, active: bool):
        self.predict_button.setEnabled(active)
        self.prediction_batch_size_spin_box.setEnabled(active)

    # endregion

    # region Layers
    def add_layer(self, layer: str):
        layer_controller = LayerController(ELayers[layer])

        layout_to_add = self.model_layers_layout.layout()
        layer_index = layout_to_add.count() - 1
        layout_to_add.insertWidget(layer_index, layer_controller.widget)

        layer_controller.ui.move_up_button.clicked.connect(lambda: self.move_layer_up(layer_controller))
        layer_controller.ui.move_down_button.clicked.connect(lambda: self.move_layer_down(layer_controller))
        layer_controller.ui.delete_button.clicked.connect(lambda: self.delete_layer(layer_controller))

        self.model_layers.append(layer_controller)
        self.check_layers_button_active()

    def open_layer_select_modal(self):
        layer_select_controller = LayerSelectController()
        layer_select_controller.ui.select_layer_button.clicked.connect(
            lambda: self.add_layer(layer_select_controller.ui.layer_select.currentData()))
        layer_select_controller.dialog.exec_()

    def move_layer_up(self, layer: LayerController):
        layers_layout = self.model_layers_layout.layout()
        index = self.model_layers.index(layer)
        layers_layout.removeWidget(layer.widget)
        layers_layout.insertWidget(index - 1, layer.widget)

        self.model_layers.insert(index - 1, self.model_layers.pop(index))

        self.check_layers_button_active()

    def move_layer_down(self, layer: LayerController):
        layers_layout = self.model_layers_layout.layout()
        index = self.model_layers.index(layer)
        layers_layout.removeWidget(layer.widget)
        layers_layout.insertWidget(index + 1, layer.widget)

        self.model_layers.insert(index + 1, self.model_layers.pop(index))

        self.check_layers_button_active()

    def delete_layer(self, layer: LayerController):
        layers_layout = self.model_layers_layout.layout()
        layers_layout.removeWidget(layer.widget)
        layers_layout.update()

        self.model_layers.remove(layer)

        self.check_layers_button_active()

    def check_layers_button_active(self):
        print()
        for i in range(len(self.model_layers)):
            print(self.model_layers[i].ui.name.text())
            self.model_layers[i].ui.move_up_button.setEnabled(i != 0)
            self.model_layers[i].ui.move_down_button.setEnabled(i != len(self.model_layers) - 1)

    def get_layers_data(self) -> dict[str: dict[str: float]]:
        return flatten_array_of_dicts(list(map(lambda item: item.get_layer_data(), self.model_layers)))

    # endregion

    # region Text updates
    def update_fitting_log(self, value: str):
        self.fitting_log.appendPlainText(value)

    def update_prediction_log(self, value: str):
        self.prediction_log.appendPlainText(value)

    def update_prediction_image(self, is_clear: bool = True, ratio: float = 1.):
        pixmap = QPixmap()
        self.predict_image.setPixmap(pixmap)

        if not is_clear:
            self.predict_image.pixmap().load('image_to_show_on_predict.jpg')
        else:
            self.predict_image.pixmap().fill(QColor(255, 255, 255))
        self.predict_image.pixmap().setDevicePixelRatio(ratio)

    def update_prediction_correct_image(self, correct=None):
        pixmap = QPixmap()
        self.predict_correct_image.setPixmap(pixmap)
        self.predict_correct_image.pixmap().setDevicePixelRatio(128)

        if correct is None:
            self.predict_correct_image.pixmap().fill(QColor(255, 255, 255))
        elif correct:
            self.predict_correct_image.pixmap().load('resources/correct_icon.png')
        else:
            self.predict_correct_image.pixmap().load('resources/incorrect_icon.png')

    def update_optimizers(self):
        self.optimizer_combo_box.clear()
        self.optimizer_combo_box.addItems(EOptimizers)
        self.optimizer_combo_box.setCurrentIndex(0)
    # endregion


def set_output_stream(stream: QRunnable):
    sys.stdout = stream


def reset_output():
    sys.stdout = sys.__stdout__
