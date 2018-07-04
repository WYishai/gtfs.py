from datetime import timedelta


def parse_timedelta(time_string):
    if isinstance(time_string, timedelta):
        return time_string

    hours, minutes, seconds = map(int, time_string.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def str_timedelta(time_delta):
    """
    :rtype: str
    :type time_delta: timedelta
    """

    total_seconds = time_delta.total_seconds()
    hours = total_seconds // (60 * 60)
    minutes = (total_seconds % (60 * 60)) // 60
    seconds = total_seconds % 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)
