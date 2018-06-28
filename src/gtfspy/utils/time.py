from datetime import timedelta


def parse_timedelta(time_string):
    if isinstance(time_string, timedelta):
        return time_string

    hours, minutes, seconds = map(int, time_string.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)
