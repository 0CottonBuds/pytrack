from Helpers.database_helper import db_find_window_by_name


class PygetwindowFilter:
    """Responsible for filtering the return value of pygetwindow.getAllWindows()"""
    def __init__(self, windows) -> None:
        self.windows = windows

    def full_filter(self):
        self.windows = self.remove_ignored_windows()
        self.windows = self.remove_windows_that_are_on_database()

    def remove_windows_that_are_on_database(self):
        filtered_windows = []

        for window in self.windows:
            splitted_name = window.title.split("- ")
            is_unique = False
            for part in splitted_name:
                result = db_find_window_by_name(part)
                if result == None:
                    is_unique = True
                    pass
                else:
                    is_unique = False
                    break
            if is_unique:
                filtered_windows.append(window)

        return filtered_windows

    def remove_ignored_windows(self) -> list:
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

        return filtered_windows

