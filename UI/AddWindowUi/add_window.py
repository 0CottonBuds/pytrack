from PySide6.QtWidgets import QWidget
from PytrackUtils.WindowUtils.window_type import WindowType
from PytrackUtils.Helpers.database_helper import record_window_type
from .ui_add_window import *


class UiAddWindow(QWidget, Ui_add_widget):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.setupUi(self)
        self.window_type = WindowType()
        self.button_confirm.clicked.connect(self.add_window_to_database)  # type:ignore
        self.button_ignore.clicked.connect(lambda delete: self.deleteLater())  # type: ignore
        combo_box_type_items = ["bad", "good"]
        self.comboBox_type.addItems(combo_box_type_items)
        combo_box_name_items = name.split("- ")
        self.comboBox_name.addItems(combo_box_name_items)

    def add_window_to_database(self):
        self.window_type.window_name = self.comboBox_name.currentText()
        self.window_type.window_type = self.comboBox_type.currentText()
        self.window_type.window_rating = int(self.lineEdit_points.text())

        record_window_type(self.window_type)

        self.deleteLater()
