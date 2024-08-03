import sqlite3

from PytrackUtils.Helpers.database_helper import find_window_on_database_by_name


class WindowType:
    def check_app_type(self, window_title : str):
        '''Takes a window checks and assign values to the instance."'''

        separated_window_title = window_title.split("- ")

        for slice in separated_window_title:
            window = find_window_on_database_by_name(slice)

            if window != None:
                self.window_name = window.window_name
                self.window_type = window.window_type
                self.window_rating = window.window_rating
                break
            else:
                pass
    def __str__(self) -> str:
        return f"name: {self.window_name}\ntype: {self.window_type}\nrating: {self.window_rating}"
