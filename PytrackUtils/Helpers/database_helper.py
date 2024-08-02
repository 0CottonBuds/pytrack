import sqlite3

from PytrackUtils.WindowUtils.window_type import WindowType

def cursor_execute(command:str, args: tuple):
    conn = sqlite3.connect("pyTrack.db")
    c = conn.cursor()

    c.execute(command, args,)

    conn.commit()
    conn.close()

def truncate_table(table:str):
    conn = sqlite3.connect("pyTrack.db")
    c = conn.cursor()

    c.execute(f"DELETE FROM {table};",)

    conn.commit()
    conn.close()

def clear_window_history():
    truncate_table("windowTimeEntries")

def clear_window_settings():
    truncate_table("windowTypes")

def record_window_time(window_name, time_elapsed):
    """enter the data to data base"""
    import datetime as dt

    conn = sqlite3.connect("pyTrack.db")

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS windowTimeEntries(windowName text, timeElapsed text, date text)""")

    today = dt.date.today()
    today = [today.year, today.month, today.day]
    date_string = f"{today[0]}-{today[1]}-{today[2]}"

    c.execute(
        """INSERT INTO windowTimeEntries VALUES(?,?,?)""",
        (window_name, str(time_elapsed), date_string),
    )

    conn.commit()

    conn.close()

    print("successfully added to database")

def record_window_type(window: WindowType):
    """enter the data to data base"""
    conn = sqlite3.connect("pyTrack.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS windowTypes(windowName text, windowType text, windowRating integer)"""
    )
    c.execute(
        """INSERT INTO windowTypes(windowName, windowType, windowRating) VALUES(?,?,?)""",
        (window.window_name, window.window_type, window.window_rating),
    )
    conn.commit()
    conn.close()
    print("successfully added to database")

def find_window_on_database_by_name(query_name: str):
    """find window on data base by name returns windowType object"""
    conn = sqlite3.connect("pyTrack.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS windowTypes(windowName text, windowType text, windowRating integer)"""
    )
    c.execute("""SELECT * FROM windowTypes WHERE windowName = ?""", (query_name,))
    results = c.fetchall()

    if results != []:
        window : WindowType = WindowType()
        window.window_name = results[0][0]
        window.window_type = results[0][1]
        window.window_rating = results[0][2]
        conn.commit()
        conn.close()
        return window

    else:
        conn.commit()
        conn.close()
        return None
