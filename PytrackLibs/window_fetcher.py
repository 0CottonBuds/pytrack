import sqlite3
import datetime as dt

from PytrackLibs.window import Window, WindowTimeElapsed, get_window_by_name

def format_windows(raw_windows: list) -> list[Window]:
    """Method for formatting windows as `Windowwindow` objects"""
    formatted_windows = []
    for entry in raw_windows:
        window = Window(entry)
        window_type = Window()
        window_type = get_window_by_name(window.name)
        window.type = window_type.type
        formatted_windows.append(window)
    return formatted_windows

def filter_formatted_windows_by_type(query_type: str, formatted_windows: list[Window]) -> list[Window]:
    """
    Parameters:
    query_type: (string) the type you want to query

    Return:
    returns a list of filtered Window objects
    """
    filtered_formatted_windows: list[Window] = []
    if query_type == "all":
        return formatted_windows

    for window in formatted_windows:
        if window.type == query_type:
            filtered_formatted_windows.append(window)

    return filtered_formatted_windows

def retrieve_all_raw_windows_by_date(date: str) -> list:
    """Method for retrieving raw windows from the database by date"""
    conn = sqlite3.connect("pyTrack.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS windowTimeEntries(windowName text, timeElapsed text, date text)""")

    c.execute("SELECT * FROM windowTimeEntries WHERE date = ?", (date,))
    raw_windows = c.fetchall()
    conn.commit()
    conn.close
    return raw_windows

def retrieve_all_raw_windows_by_many_dates(dates: list[str]) -> list:
    raw_windows = []
    for date in dates:
        curr_windows = retrieve_all_raw_windows_by_date(date) 
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

def get_total_time_elapsed(formatted_windows: list[Window]) -> WindowTimeElapsed:
    """Calculate the total time elapsed.

    Args:
        formatted_windows: A list of window windows.

    Returns:
        The total time elapsed as a WindowTimeElapsed object.
    """
    total_time = WindowTimeElapsed(f"0, 0, 0")

    for entry in formatted_windows:
        total_time += entry.time_elapsed
    return total_time

def get_time_of_each_window(
    formatted_windows: list[Window],
) -> list[Window]:
    """get time elapsed on each window"""
    unique_windows: list[Window] = []

    for entry in formatted_windows:

        is_unique: bool = True
        for window in unique_windows:
            if window.short_name == entry.short_name:
                is_unique = False
                window.time_elapsed += entry.time_elapsed
        if is_unique:
            unique_window = entry
            unique_windows.append(unique_window)

    return unique_windows

def get_percentage_of_time_of_each_window(
    formatted_windows: list[Window],
) -> list[Window]:
    """
    Calculates the percentage of time spent on each window and adds this information to the list of window windows.

    Parameters:
        formatted_windows (List[Windowwindow]): A list of window windows containing information about the time spent on each window.

    Returns:
        List[Windowwindow]: A list of window windows with the percentage of time spent on each window added.
    """
    total_time: WindowTimeElapsed = get_total_time_elapsed(formatted_windows)
    time_of_each_window: list[Window] = get_time_of_each_window(formatted_windows)

    total_time_in_seconds = total_time.hours * 3600
    total_time_in_seconds += total_time.minutes * 60
    total_time_in_seconds += total_time.seconds

    percentages: list[Window] = []  # this will be the returned list

    for window in time_of_each_window:
        percentage = 0

        window_time_in_seconds = window.time_elapsed.hours * 3600
        window_time_in_seconds += window.time_elapsed.minutes * 60
        window_time_in_seconds += window.time_elapsed.seconds

        percentage = window_time_in_seconds and window_time_in_seconds / total_time_in_seconds or 0
        percentage = percentage * 100

        window.time_elapsed.percentage = round(percentage, 2)

        percentages.append(window)

    return percentages

