from Helpers.database_helper import find_window_on_database_by_name


class Window:
    """class to handle and store data that is retrieved from the database"""

    short_name: str = ""
    name: str = ""
    type: str = ""
    rating: int = 0

    def __init__(self, entry = []):
        if entry == []:
            return
        window_name: str = entry[0]
        time_elapsed: str = entry[1]
        date_entered: str = entry[2]

        split_window_name = window_name.split("- ")

        self.short_name: str = split_window_name[-1]
        self.name: str = window_name
        self.time_elapsed = WindowTime(time_elapsed)
        self.date_entered = date_entered

    def __str__(self) -> str:
        return f"name: {self.name}\ntype: {self.type}\nrating: {self.rating}"

class WindowTime:
    """class window time for keeping data(time)"""

    name: str
    full_name: str
    percentage: float

    def __init__(self, time_elapsed: str) -> None:
        split_time_elapsed = time_elapsed.split(", ")

        self.hours: float = float(split_time_elapsed[0])
        self.minutes: float = float(split_time_elapsed[1])
        self.seconds: float = float(split_time_elapsed[2])

        self.format_time()

    def get_time(self) -> tuple:
        """returns tuple of time"""
        self.format_time()
        time = (self.hours, self.minutes, self.seconds)
        return time

    def format_time(self):
        """formats the time to avoid the negatives and time going above 60 \n use this when changing the time value"""
        if self.minutes > 60:
            self.minutes -= 60
            self.hours += 1
        if self.seconds > 60:
            self.seconds -= 60
            self.minutes += 1
        if self.seconds < 0:
            self.seconds += 60
        if self.minutes < 0:
            self.minutes += 60

    def __add__(self, other: "WindowTime") -> "WindowTime":
        self.hours = self.hours + other.hours
        self.minutes = self.minutes + other.minutes
        self.seconds = self.seconds + other.seconds

        self.format_time()

        return WindowTime(f"{self.hours}, {self.minutes}, {self.seconds}")

def check_app_type(window_title : str):
    '''Takes a window checks and assign values to the instance."'''

    separated_window_title = window_title.split("- ")

    for slice in separated_window_title:
        window = find_window_on_database_by_name(slice)

        if window != None:
            return window

    return Window()

