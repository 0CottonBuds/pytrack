from PySide6.QtCore import Slot

from Helpers.notification_helper import notify_break, notify_back_to_work 
from Helpers.config_helper import read_config


class PointTracker:
    """Tracks points and calls notifications when threshold is met"""
    points: int

    def __init__(self) -> None:
        self.config_file_read_points_settings()
        self.points = self.starting_points

    @Slot()
    def change_points(self, window_type, window_points):
        """add and subtracts points based on window type. \n"""

        if window_type == "good":
            self.points += window_points
            print(f"added {window_points} points\ntotal points: {self.points}")
        elif window_type == "bad":
            self.points -= window_points
            print(f"subtract {window_points} points\ntotal points: {self.points}")
        else:
            print("this window does not have a label")
        
        self.check_point_threshold()
        print(self)

    def check_point_threshold(self):
        self.config_file_read_points_settings()

        if self.points >= self.break_threshold:
            notify_break()
        if self.points <= self.warning_threshold:
            notify_back_to_work()

    def config_file_read_points_settings(self):
        
        self.starting_points = int(read_config(r"./config.ini", "App", "starting_points" ))
        self.warning_threshold = int(read_config(r"./config.ini", "App", "warning_threshold" ))  # type: ignore
        self.break_threshold = int(read_config(r"./config.ini", "App", "break_threshold" ))

    def __str__(self) -> str:
        return f"Points: {self.points}"


if __name__ == "__main__":
    point = PointTracker()
    point.points = 0
    point.check_point_threshold()
