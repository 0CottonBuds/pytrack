import datetime as dt

from PytrackLibs.window import Window, WindowTimeElapsed, get_window_by_name
from Helpers.database_helper import db_find_raw_window_time_entries_by_date

"""responsible for using database helper functions to get raw window data and serialize them to Window objects"""

def format_windows(raw_windows: list) -> list[Window]:
    formatted_windows = []
    for entry in raw_windows:
        window = Window(entry)
        window_type = Window()
        window_type = get_window_by_name(window.name)
        window.type = window_type.type
        formatted_windows.append(window)
    return formatted_windows

def filter_windows_by_type(query_type: str, formatted_windows: list[Window]) -> list[Window]:
    """
    Parameters:
        query_type : str = the type you want to query

    Return:
        list[Window] = filtered windows
    """
    filtered_formatted_windows: list[Window] = []
    if query_type == "all":
        return formatted_windows

    for window in formatted_windows:
        if window.type == query_type:
            filtered_formatted_windows.append(window)

    return filtered_formatted_windows

def get_all_raw_windows_by_dates(dates: list[str]) -> list:
    raw_windows = []
    for date in dates:
        curr_windows = db_find_raw_window_time_entries_by_date(date) 
        raw_windows.extend(curr_windows)
    return raw_windows

def get_dates(query: str = "today") -> list:
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

    return list_of_dates




#TODO: move to other file


def get_total_elapsed_time_of_windows(
    formatted_windows: list[Window],
) -> list[Window]:
    """
    Parameters:
        formatted_windows: list[Window] = list of windows with duplicates with same name

    Returns:
        list[Window] = combines windows with the same name and adds their elapsed time
    """
    unique_windows: list[Window] = []

    for window in formatted_windows:

        is_unique: bool = True
        for unique_window in unique_windows:
            if unique_window.short_name == window.short_name:
                is_unique = False
                unique_window.time_elapsed += window.time_elapsed
        if is_unique:
            unique_windows.append(window)

    return unique_windows

def get_time_percentage_of_windows(
    formatted_windows: list[Window],
) -> list[Window]:
    """
    Parameters:
        formatted_windows : List[Window] = A list of window with elapsed times.

    Returns:
        List[Window]: modified formatted_windows with percentage.
    """

    total_time = WindowTimeElapsed(f"0, 0, 0")
    for entry in formatted_windows:
        total_time += entry.time_elapsed

    total_time_in_seconds = total_time.hours * 3600
    total_time_in_seconds += total_time.minutes * 60
    total_time_in_seconds += total_time.seconds

    time_of_each_window: list[Window] = get_total_elapsed_time_of_windows(formatted_windows)

    windows_with_percentages: list[Window] = []
    for window in time_of_each_window:
        percentage = 0

        window_time_in_seconds = window.time_elapsed.hours * 3600
        window_time_in_seconds += window.time_elapsed.minutes * 60
        window_time_in_seconds += window.time_elapsed.seconds

        percentage = window_time_in_seconds and window_time_in_seconds / total_time_in_seconds or 0
        percentage = percentage * 100

        window.time_elapsed.percentage = round(percentage, 2)

        windows_with_percentages.append(window)

    return windows_with_percentages

