from PySide6.QtWidgets import QWidget

from .ui_window_record import *


class Ui_Window_Record(QWidget, Ui_window_record):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
