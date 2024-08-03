import pygetwindow as gw
import datetime as dt

from PySide6.QtCore import QObject, Signal

from Helpers.database_helper import record_window_time 
from PyTrack.window import Window, check_app_type

class PyTrack(QObject):
    time_started: tuple
    time_finished: tuple
    points_changed: Signal = Signal(str, int)

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.last_active_window = None
        self.time_started = self.get_time_now()
        self.time_finished = (0, 0, 0)

    def main_loop(self):
        self.current_active_window = gw.getActiveWindow()

        if self.last_active_window is None:
            self.last_active_window = self.current_active_window

        # this is a loop so every time we loop we consider that this is the time finished
        self.time_finished = self.get_time_now() 

        window = Window()
        window = check_app_type(self.current_active_window.title)

        # we emit so point tracker on App class can change points and ui label to change
        self.points_changed.emit(window.type, window.rating)

        print(f"Active Window: {window}")

        # checks if window changed if it changes it records the data to the
        # database if all prerequisite parameters exists
        is_window_changed = self.current_active_window != self.last_active_window
        if is_window_changed:
            is_parameters_complete = (
                self.time_finished is not None and 
                self.time_started is not None and
                self.last_active_window is not None
            )
            if is_parameters_complete:
                record_window_time(self.last_active_window.title, self.get_total_window_time())

            # this is here cuz we need to record window time fisst before altering the time start
            self.last_active_window = self.current_active_window
            self.time_started = self.get_time_now()


        print(self.get_total_window_time())

    def get_total_window_time(self) -> tuple:
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

