import plyer


def notify_break():
    plyer.notification.notify(
        title="Hey bud, Take a break you've been working too hard.",
        message="You've been working too hard. Don't forget that taking breaks is beneficial for productivity!",
        app_icon=r"Icons\break.ico",
        timeout=10,
    )  # type: ignore

def notify_back_to_work():
    plyer.notification.notify(
        title="Get back to work!!",
        message="You've been procrastinating and your points are super low, Get back to work.",
        app_icon=r"Icons\warning.ico",
        timeout=10,
    )  # type: ignore
