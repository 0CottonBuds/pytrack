from Helpers.database_helper import db_find_window_by_name


class Window:
    """"""

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
        self.time_elapsed = WindowTimeElapsed(time_elapsed)
        self.date_entered = date_entered

    def __str__(self) -> str:
        return f"name: {self.name}\ntype: {self.type}\nrating: {self.rating}"

class WindowTimeElapsed:
    hours: float
    minutes: float
    seconds: float
    percentage: float

    def __init__(self, time_elapsed: str) -> None:
        split_time_elapsed = time_elapsed.split(", ")

        self.hours: float = float(split_time_elapsed[0])
        self.minutes: float = float(split_time_elapsed[1])
        self.seconds: float = float(split_time_elapsed[2])

        self.handle_negative()

    def to_tuple(self) -> tuple:
        self.handle_negative()
        return (self.hours, self.minutes, self.seconds)    
    
    def handle_negative(self):
        """handles the negatives values and values going above their respective limit(24, 60, 60)"""
        while self.minutes > 60:
            self.minutes -= 60
            self.hours += 1
        while self.seconds > 60:
            self.seconds -= 60
            self.minutes += 1
        while self.seconds < 0:
            self.seconds += 60
            self.minutes -= 1
        while self.minutes < 0:
            self.minutes += 60
            self.hours -= 1

    def __add__(self, other: "WindowTimeElapsed") -> "WindowTimeElapsed":
        self.hours = self.hours + other.hours
        self.minutes = self.minutes + other.minutes
        self.seconds = self.seconds + other.seconds

        self.handle_negative()

        return WindowTimeElapsed(f"{self.hours}, {self.minutes}, {self.seconds}")

def get_window_by_name(window_name : str) -> Window:

    # we do this because pygetwindow gives window names like operagx - youtube.com
    separated_window_name = window_name.split("- ")

    for slice in separated_window_name:
        window = db_find_window_by_name(slice)

        if window != None:
            return window

    return Window()

