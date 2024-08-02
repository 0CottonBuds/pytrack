import sqlite3
import datetime as dt
from .window_type import *


class WindowRecord:
    """class to handle and store data that is retrieved from the database"""

    window_type: str

    def __init__(self, entry):
        window_name: str = entry[0]
        time_elapsed: str = entry[1]
        date_entered: str = entry[2]

        split_window_name = window_name.split("- ")

        self.window_short_name: str = split_window_name[-1]
        self.window_full_name: str = window_name
        self.window_time_elapsed = WindowTime(time_elapsed)
        self.window_date_entered = date_entered


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


class WindowRecordFetcher:
    """Class that fetches the data and formats it\n
    -> list[WindowRecords]"""

    formatted_records: list[WindowRecord] = []

    def fetch_all_records(self):
        """combination of format_raw_entries and retrieve_raw_entries as one function"""
        self.formatted_records = self.format_records(self.retrieve_all_raw_records())

    def fetch_records_by_date(self, date: str):
        """combination of format_raw_entries and retrieve_raw_entries as one function but with dates"""
        self.formatted_records = self.format_records(self.retrieve_all_raw_records_by_date(date))

    def format_records(self, raw_records: list) -> list[WindowRecord]:
        """Method for formatting records as `WindowRecord` objects"""
        formatted_records = []
        for entry in raw_records:
            record = WindowRecord(entry)
            record_type = WindowType()
            record_type.check_app_type(record.window_full_name)
            record.window_type = record_type.window_type
            formatted_records.append(record)
        self.formatted_records = formatted_records
        return formatted_records

    def filter_formatted_records_by_type(self, query_type: str) -> list[WindowRecord]:
        """function to filter WindowRecord objects by their type

        Parameters:
        query_type: (string) the type you want to query

        Return:
        returns a list of filtered WindowRecord objects

        TODO: this function is untested
        """
        filtered_formatted_records: list[WindowRecord] = []
        if query_type != "all":
            for record in self.formatted_records:
                if record.window_type == query_type:
                    filtered_formatted_records.append(record)
                else:
                    pass
        else:
            return self.formatted_records
        self.formatted_records = filtered_formatted_records
        return filtered_formatted_records

    def retrieve_all_raw_records(self) -> list:
        """Method for retrieving all raw records from the database"""
        conn = sqlite3.connect("pyTrack.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS windowTimeEntries(windowName text, timeElapsed text, date text)""")

        c.execute("SELECT * FROM windowTimeEntries")
        raw_records = c.fetchall()
        conn.commit()
        conn.close
        return raw_records

    def retrieve_all_raw_records_by_date(self, date: str) -> list:
        """Method for retrieving raw records from the database by date"""
        conn = sqlite3.connect("pyTrack.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS windowTimeEntries(windowName text, timeElapsed text, date text)""")

        c.execute("SELECT * FROM windowTimeEntries WHERE date = ?", (date,))
        raw_records = c.fetchall()
        conn.commit()
        conn.close
        return raw_records

    def retrieve_all_raw_records_by_many_dates(self, dates: list[str]) -> list:
        # TODO: this function is untested test as soon as possible
        raw_records = []
        for date in dates:
            raw_records.extend(self.retrieve_all_raw_records_by_date(date))
        return raw_records

    def get_dates(self, query: str = "today") -> list:
        """
        Retrieves dates based on the given query.

        Parameters:
            Query: (String) today, yesterday, this week, this month, etc

        Returns:
            list: A list of dates that match the given query (today, yesterday, this week, or this month).

        TODO: This function is untested and have a known bug
        """

        def list_to_strings(date) -> str:
            """turns date(tuple) to string"""
            date_string = f"{date[0]}-{date[1]}-{date[2]}"
            return date_string

        def handle_negatives(date: list) -> list:
            """handles the negative numbers that subtracting may cause"""
            # TODO: this function has a bug, because this function dont know if it is supposed to add 30 or 31 to the day. we just assume it's 30.
            date_revised = date
            if date_revised[2] < 1:
                date_revised[2] += 30
                date_revised[1] -= 1
            if date_revised[1] < 1:
                date_revised[1] += 12
                date_revised[0] -= 1
            if date_revised[0] < 1:
                print("man we exceeded the min limit of the year.")
                pass
            return date_revised

        list_of_dates = []
        today = dt.date.today()
        today = [today.year, today.month, today.day]

        if query == "today":
            list_of_dates.append(list_to_strings(today))
        elif query == "yesterday":
            yesterday = [today[0], today[1], today[2] - 1]
            yesterday = handle_negatives(yesterday)
            list_of_dates.append(list_to_strings(yesterday))
        elif query == "this week":
            latest_day = today
            list_of_dates.append(list_to_strings(latest_day))

            for i in range(1, 8):
                day_before = latest_day
                day_before[2] -= 1
                day_before = handle_negatives(day_before)
                list_of_dates.append(list_to_strings(day_before))
                latest_day = day_before
        elif query == "this month":
            latest_day = today
            list_of_dates.append(list_to_strings(latest_day))

            for i in range(1, 31):
                day_before = latest_day
                day_before[2] -= 1
                day_before = handle_negatives(day_before)
                list_of_dates.append(list_to_strings(day_before))
                latest_day = day_before
        else:
            pass

        return list_of_dates

    def __str__(self) -> str:
        message = ""

        for records in self.formatted_records:
            message += f"{records.window_full_name}, {records.window_time_elapsed.get_time()} \n"
        return message


def get_total_time_elapsed(formatted_records: list[WindowRecord]) -> WindowTime:
    """Calculate the total time elapsed.

    Args:
        formatted_records: A list of window records.

    Returns:
        The total time elapsed as a WindowTime object.
    """
    total_time = WindowTime(f"0, 0, 0")

    # Iterate over the records and add the elapsed time for each record to the total time.
    for entry in formatted_records:
        total_time += entry.window_time_elapsed
    return total_time


def get_time_of_each_window(
    formatted_records: list[WindowRecord],
) -> list[WindowRecord]:
    """get time elapsed on each window"""
    unique_windows: list[WindowRecord] = []

    # loop through the entries
    for entry in formatted_records:

        # loop through the unique window list find if there is a match or not
        is_unique: bool = True
        for window in unique_windows:
            # if not unique add time elapsed to the object that it matched
            if window.window_short_name == entry.window_short_name:
                is_unique = False
                window.window_time_elapsed += entry.window_time_elapsed
            else:
                pass

        # if unique then add a new item in the list
        if is_unique:
            unique_window = entry
            unique_windows.append(unique_window)

    return unique_windows


def get_percentage_of_time_of_each_window(
    formatted_records: list[WindowRecord],
) -> list[WindowRecord]:
    """
    Calculates the percentage of time spent on each window and adds this information to the list of window records.

    Parameters:
        formatted_records (List[WindowRecord]): A list of window records containing information about the time spent on each window.

    Returns:
        List[WindowRecord]: A list of window records with the percentage of time spent on each window added.
    """
    total_time: WindowTime = get_total_time_elapsed(formatted_records)
    time_of_each_window: list[WindowRecord] = get_time_of_each_window(formatted_records)

    total_time_in_seconds = total_time.hours * 3600
    total_time_in_seconds += total_time.minutes * 60
    total_time_in_seconds += total_time.seconds

    percentages: list[WindowRecord] = []  # this will be the returned list

    for window in time_of_each_window:
        percentage = 0

        window_time_in_seconds = window.window_time_elapsed.hours * 3600
        window_time_in_seconds += window.window_time_elapsed.minutes * 60
        window_time_in_seconds += window.window_time_elapsed.seconds

        percentage = window_time_in_seconds and window_time_in_seconds / total_time_in_seconds or 0
        percentage = percentage * 100

        window.window_time_elapsed.percentage = round(percentage, 2)

        percentages.append(window)

    return percentages


if __name__ == "__main__":
    records = WindowRecordFetcher()
    records.fetch_all_records()
    records = records.formatted_records
    # print(records)

    total_time_elapsed = get_total_time_elapsed(records)
    print(total_time_elapsed.get_time())
    print()

    time_of_each_window = get_time_of_each_window(records)

    for window in time_of_each_window:
        print(window.window_full_name)
        print(window.window_time_elapsed.get_time())

    percentage_time_of_each_window = get_percentage_of_time_of_each_window(records)

    full_percentage = 0
    for window in percentage_time_of_each_window:
        print(f"name: {window.window_short_name}")
        print(f"percentage: {window.window_time_elapsed.percentage}")
        full_percentage += window.window_time_elapsed.percentage
    print(round(full_percentage, 2))
    pass
