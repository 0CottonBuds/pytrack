from PytrackUtils.Helpers.database_helper import find_window_on_database_by_name

"""This is responsible for filtering the return value of pygetwindow."""

class Win32Filter:
    '''WindowFilter class is used for filtering WindowType class entries on the database see WindowType's documentation.'''
    def __init__(self, windows) -> None:
        self.windows = windows

    def full_filter(self):
        """uses all the filter in the class"""

        self.filter_ignored_windows()
        self.filter_windows_that_are_on_database()

    def filter_windows_that_are_on_database(self):
        """cycles to the list of windows(Input) and checks if there is an entry of that window"""
        filtered_windows = []

        for window in self.windows:
            splitted_name = window.title.split("- ")
            is_unique = False
            for part in splitted_name:
                result = find_window_on_database_by_name(part)
                if result == None:
                    is_unique = True
                    pass
                else:
                    is_unique = False
                    break
            if is_unique:
                filtered_windows.append(window)

        self.windows = filtered_windows
        return filtered_windows

    def filter_ignored_windows(self) -> list:
        """filters the windows that you want to ignore and returns a list of windows"""
        filtered_windows = []
        ignored_window_names = [
            "",
            "Settings",
            "Microsoft Text Input Application",
            "Program Manager",
            "Clock",
            "Setup",
            "Calculator",
        ]

        for window in self.windows:
            splitted_title: list[str] = window.title.split("- ")
            # print(window.title)
            if splitted_title[-1] in ignored_window_names:
                # print(f"this window is ignored name: {window.title}")
                pass
            else:
                filtered_windows.append(window)

        self.windows = filtered_windows
        return filtered_windows

