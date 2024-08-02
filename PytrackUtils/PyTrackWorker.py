import pygetwindow as gw
import datetime as dt

from PySide6.QtCore import QObject

from PytrackUtils.Helpers.database_helper import record_window_time 
from PytrackUtils.point_tracker import PointTracker 
from PytrackUtils.WindowUtils.window_type import WindowType

class PyTrackWorker(QObject):
    time_started: tuple
    time_finished: tuple

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.last_active_window = None
        self.time_started = self.get_time_now()
        self.time_finished = (0, 0, 0)
        self.point_tracker = PointTracker()

    def main_loop(self):
        self.current_active_window = gw.getActiveWindow()

        if self.last_active_window is None:
            self.last_active_window = self.current_active_window

        self.time_finished = self.get_time_now() 

        # check app type
        window = WindowType()
        window.check_app_type(self.current_active_window.title)

        # change points
        self.point_tracker.change_points(window.window_type, window.window_rating)
        self.point_tracker.check_point_threshold()

        print(f"Active Window: {window}")
        print(self.point_tracker)
        self.main_window.label_points_home.setText(str(self.point_tracker))

        """checks if window changed if it changes it records the data to the
        database if all prerequisite parameters exists"""
        is_window_changed = self.current_active_window != self.last_active_window
        if is_window_changed:
            self.last_active_window = self.current_active_window
            self.time_started = self.get_time_now()

            is_parameters_complete = (
                self.time_finished is not None and 
                self.time_started is not None and
                self.last_active_window is not None
            )
            if is_parameters_complete:
                record_window_time(self.last_active_window.title, self.get_total_elapsed_time())

        print(self.get_total_elapsed_time())

    def get_total_elapsed_time(self) -> tuple:
        """function to subtract two time(hours, minutes, seconds)\n
        returns tuple(Hours, Minutes, Seconds)\n
        check TODO to see bugs"""

        """ TODO: fix bug that make this function act weird when we are subtracting from another 12 hour cycle i.e.: 11pm - 12am(00:00) which results this function to make large numbers i.e.: -23,-58,-30"""

        hours: float = self.time_finished[0] - self.time_started[0]
        minutes: float = self.time_finished[1] - self.time_started[1]
        seconds: float = self.time_finished[2] - self.time_started[2]

        # check if the time became negative and compensate
        if seconds < 0:
            minutes -= 1
            seconds += 60
        if minutes < 0:
            hours -= 1
            minutes += 60

        time_elapsed = (hours, minutes, seconds)
        return time_elapsed

    def get_time_now(self):
        time_now = dt.datetime.now()
        return (time_now.hour, time_now.minute, time_now.second)


