from datetime import timedelta


def parse_timedelta(time_string):
    if time_string is None or time_string == '':
        return None

    hours, minutes, seconds = map(int, time_string.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)
