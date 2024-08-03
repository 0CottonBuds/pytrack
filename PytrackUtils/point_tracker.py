from PySide6.QtCore import Slot

from .Helpers.notification_helper import notify_break, notify_back_to_work 
import configparser


class PointTracker:
    points: int

    def __init__(self) -> None:
        self.read_settings_config_file()
        self.points = self.starting_points

    @Slot()
    def change_points(self, window_type, window_points):
        """add and subtracts points based on app type. \n"""

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
        """check point threshold. \n
        calls the notification module to fire notification when threshold is reached."""
        self.read_settings_config_file()

        if self.points >= self.threshold_break:
            notify_break()
        if self.points <= self.threshold_warning:
            notify_back_to_work()

    def read_settings_config_file(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(r".\config.ini")  # type: ignore

        self.starting_points = int(config_parser["App"]["starting_points"])
        self.threshold_warning = int(config_parser["App"]["warning_threshold"])  # type: ignore
        self.threshold_break = int(config_parser["App"]["break_threshold"])

    def __str__(self) -> str:
        return f"Points: {self.points}"


if __name__ == "__main__":
    point = PointTracker()
    point.points = 0
    point.check_point_threshold()
