from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon
from PySide6.QtCore import QTimer, Qt
from PySide6 import QtCore
from PySide6.QtGui import Qt, QIcon
from PySide6.QtCharts import QChartView, QChart, QLineSeries

import sys
import pygetwindow

from GUI.Main.main_ui import Ui_MainWindow
from GUI.WindowRecordUi.window_record import Ui_Window_Record
from GUI.AddWindowUi.add_window import UiAddWindow

from PytrackLibs.window import Window
from PytrackLibs.pygetwindow_filter import PygetwindowFilter
from PytrackLibs.window_fetcher import format_windows, filter_windows_by_type, get_all_raw_windows_by_dates, get_dates, get_total_elapsed_time_of_windows, get_time_percentage_of_windows
from PytrackLibs.point_tracker import PointTracker
from PytrackLibs.pytrack import PyTrack 

from Helpers.webbrowser_helper import go_to_link_github, go_to_link_github_repository, go_to_link_twitter, go_to_link_youtube_channel, go_to_link_youtube_video
from Helpers.stylesheet_helper import change_stylesheet, get_themes
from Helpers.config_helper import edit_config, read_config
from Helpers.database_helper import clear_window_history, clear_window_settings

from pytrack_system_tray import setup_system_tray

class App(QMainWindow, Ui_MainWindow):
    main_loop_active : bool
    pytrack_worker : PyTrack
    point_tracker : PointTracker
    main_loop_activated: bool

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Pytrack")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # type: ignore

        self.pytrack_worker = PyTrack(self)
        self.point_tracker = PointTracker()

        self.pytrack_worker.points_changed.connect(self.point_tracker.change_points)
        self.pytrack_worker.points_changed.connect(lambda x, y: self.label_points_home.setText(self.point_tracker.__str__()))

        self.main_loop_active = False

        self.place_holder_text_init()
        self.combo_box_items_init()
        self.charts_init()
        self.timers_init()

        self.buttons_init()
        self.text_edit_init()
        self.combo_box_signals_init()

        # set stylesheet as the first one on the list by default
        change_stylesheet(self, read_config("config.ini", "App", "theme"), app)
        
        self.show()

    ###INIT FUNCTIONS ###

    def place_holder_text_init(self):
        self.button_activate_deactivate_main_loop.setText("Activate")
        self.line_edit_point_threshold_break.setPlaceholderText(str(self.point_tracker.break_threshold))
        self.line_edit_point_threshold_warning.setPlaceholderText(str(self.point_tracker.warning_threshold))

    def combo_box_items_init(self):
        combo_box_date_items = ["today", "yesterday", "this week", "this month", "all"]
        self.comboBox_date.addItems(combo_box_date_items)
        combo_box_type_items = ["all", "bad", "good"]
        self.comboBox_type.addItems(combo_box_type_items)
        self.get_records("today", "all")
        combo_box_theme_items = get_themes()
        self.comboBox_theme.addItems(combo_box_theme_items)
    
    def charts_init(self):
        self.point_line_series = QLineSeries()
        self.point_line_series.append(0, self.point_tracker.points / 10)
        chart = QChart()
        chart.addSeries(self.point_line_series)
        chart.setTitle("Points Over Time")

        self.chart_view = QChartView()
        self.chart_view.setChart(chart)
        self.point_graph_container_layout.addWidget(self.chart_view)

    def timers_init(self):
        self.main_loop_timer = QTimer()
        self.point_graph_timer = QTimer()

        self.main_loop_timer.timeout.connect(self.pytrack_worker.main_loop)  # type: ignore
        self.point_graph_timer.timeout.connect(self.add_point_to_point_chart)

    def buttons_init(self):
        self.button_activate_deactivate_main_loop.clicked.connect(self.main_loop_switch)  # type: ignore

        self.button_go_to_home.clicked.connect( lambda: self.stackedWidget.setCurrentWidget(self.page_home))  # type: ignore
        self.button_go_to_analytics.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_analytics))  # type: ignore
        self.button_go_to_settings.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_settings))  # type: ignore
        self.button_settings_general.clicked.connect(lambda: self.page_settings_stacked_widget.setCurrentWidget(self.page_settings_stacked_widget_page_general))  # type: ignore
        self.button_settings_window.clicked.connect(lambda: self.page_settings_stacked_widget.setCurrentWidget(self.page_settings_stacked_widget_page_window))  # type: ignore
        self.button_settings_about.clicked.connect(lambda: self.page_settings_stacked_widget.setCurrentWidget(self.page_settings_stacked_widget_page_about))  # type: ignore

        self.button_link_to_twitter.clicked.connect(go_to_link_twitter)  # type: ignore
        self.button_link_to_github.clicked.connect(go_to_link_github)  # type: ignore
        self.button_link_to_youtube_video.clicked.connect(go_to_link_youtube_video)  # type: ignore
        self.button_link_to_youtube_channel.clicked.connect(go_to_link_youtube_channel)  # type: ignore
        self.button_link_to_github_repository.clicked.connect(go_to_link_github_repository)  # type: ignore

        self.button_add_windows.clicked.connect(self.create_add_window_ui)  # type: ignore
        self.button_clear_window_history.clicked.connect(clear_window_history)
        self.button_clear_window_settings.clicked.connect(clear_window_settings)

        self.button_exit.clicked.connect(lambda q: sys.exit())
        self.button_minimize.clicked.connect(lambda m: self.showMinimized())

    def text_edit_init(self):
        # setting the text edit signals to slots
        self.line_edit_point_threshold_break.editingFinished.connect(self.edit_break_threshold_points)  # type: ignore
        self.line_edit_point_threshold_warning.editingFinished.connect(self.edit_warning_threshold_points)  # type: ignore

    def combo_box_signals_init(self):
        # set combo box signals to slots
        self.comboBox_date.currentTextChanged.connect(self.on_date_combo_box_update)  # type: ignore
        self.comboBox_type.currentTextChanged.connect(self.on_typecombo_box_update)  # type: ignore
        self.comboBox_theme.currentTextChanged.connect(self.on_theme_combo_box_update) # type: ignore

    ### CONFIG FUNCTIONS ###

    def edit_break_threshold_points(self):

        value = self.line_edit_point_threshold_break.text()
        if value == "":
            value: str = str(self.point_tracker.break_threshold)  # type: ignore bypass formatting

        if value.isnumeric():
            print(f"changing point threshold for break to {value}")

            edit_config("./config.ini", "App", "break_threshold", value)
            self.point_tracker.config_file_read_points_settings()

            # Set line edit placeholder text.
            self.line_edit_point_threshold_break.setPlaceholderText(str(self.point_tracker.break_threshold))
            self.line_edit_point_threshold_break.clear()
        else:
            print(f"tried to input {value} but it is not numeric.")

            # Set line edit placeholder text.
            self.line_edit_point_threshold_break.setPlaceholderText(str(self.point_tracker.break_threshold))
            self.line_edit_point_threshold_break.clear()

    def edit_warning_threshold_points(self):
        value: str = self.line_edit_point_threshold_warning.text()
        if value == "":
            value = str(self.point_tracker.warning_threshold)  # type: ignore bypass formatting

        if value.isnumeric():
            print(f"changing point threshold for warning to {value}")

            edit_config("./config.ini", "App", "warning_threshold", value)
            self.point_tracker.config_file_read_points_settings()

            # Set line edit placeholder text.
            self.line_edit_point_threshold_warning.setPlaceholderText(str(self.point_tracker.warning_threshold))
            self.line_edit_point_threshold_warning.clear()
        else:
            print(f"tried to input {value} but it is not numeric.")

            # Set line edit placeholder text.
            self.line_edit_point_threshold_warning.setPlaceholderText(str(self.point_tracker.warning_threshold))
            self.line_edit_point_threshold_warning.clear()

    ### UI FUNCTIONS ###

    def on_date_combo_box_update(self, text):
        print(f"signal: {text}")
        self.get_records(self.comboBox_date.currentText(), self.comboBox_type.currentText())

    def on_typecombo_box_update(self, text):
        print(f"signal: {text}")
        self.get_records(self.comboBox_date.currentText(), self.comboBox_type.currentText())

    def on_theme_combo_box_update(self, text):
        change_stylesheet(self, text, app)
        edit_config("config.ini", "App", "theme", text)

    def add_point_to_point_chart(self):
        count = self.point_line_series.count()
        points = self.point_tracker.points / 10  # points divided by 10
        self.point_line_series.append(count, points)
        self.update_chart_view()
        print(f"adding points: {count}, {points}")

    def update_chart_view(self):
        chart = QChart()
        chart.addSeries(self.point_line_series)
        chart.setTitle("Points Over Time")
        self.chart_view.setChart(chart)

    def update_window_time_history(self, windows: list[Window]):
        """        
        Parameters:
            records: list[WindowRecord] = list of windows"""

        # clears the scroll area
        for i in reversed(range(self.scroll_area_contents_layout.count())):
            self.scroll_area_contents_layout.itemAt(i).widget().setParent(None)  # type: ignore

        print("updating contents")
        for record in windows:
            obj = Ui_Window_Record()
            obj.label_name.setText(record.short_name)
            obj.label_total_time.setText(str(record.time_elapsed.to_tuple()))
            obj.progressBar.setValue(int(record.time_elapsed.percentage))

            self.scroll_area_contents_layout.addWidget(obj)
            self.scroll_area_contents_layout.setAlignment(obj, Qt.AlignmentFlag.AlignTop)

    def create_add_window_ui(self):
        """Creates UIAddWindow"""
        window_filter = PygetwindowFilter(pygetwindow.getAllWindows())
        window_filter.full_filter()

        # clear the add window contents layout
        for i in reversed(range(self.add_window_contents_layout.count())):
            self.add_window_contents_layout.itemAt(i).widget().setParent(None)  # type: ignore

        for window in window_filter.windows:
            add_window_ui = UiAddWindow(window.title)
            self.add_window_contents_layout.addWidget(add_window_ui)

    ### PYTRACK FUNCTIONS ###
    
    def main_loop_switch(self):
        if not self.main_loop_active:
            print("Activated")
            self.main_loop_timer.start(5000)
            self.point_graph_timer.start(5000)
            self.main_loop_active = True
            self.button_activate_deactivate_main_loop.setText("Deactivate")
        elif self.main_loop_active:
            print("Deactivated")
            self.main_loop_timer.stop()
            self.point_graph_timer.stop()
            self.main_loop_active = False
            self.button_activate_deactivate_main_loop.setText("Activate")

    def get_records(self, query_date: str, query_type: str):
        """Updates window time history based on query type

        Parameters:
            query_date: str = date to query ex. today, yesterday, etc
            query_type: str = type to query ex. good, bad, all"""

        print("getting records")
        windows: list[Window] = []
        formatted_windows = []

        dates = get_dates(query_date)
        raw_windows = get_all_raw_windows_by_dates(dates) 

        formatted_windows = format_windows(raw_windows)
        filtered_windows = filter_windows_by_type(query_type, formatted_windows)

        windows = filtered_windows 
        windows = get_total_elapsed_time_of_windows(windows)
        windows = get_time_percentage_of_windows(windows)

        self.update_window_time_history(windows)

    ### WINDOW FUNCTIONS ###

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(), self.mapToGlobal(self.movement).y(), self.width(), self.height())
            self.start = self.end

    def mouseReleaseEvent(self, event):
        self.pressing = False


if __name__ == "__main__":
    app = QApplication()
    window = App()

    app.setQuitOnLastWindowClosed(False)
    
    system_tray_icon = QIcon("Assets\Icons\icon.ico")

    if QSystemTrayIcon.isSystemTrayAvailable():
        setup_system_tray(app, window)

    app.exec()
