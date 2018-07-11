def str_to_bool(value):
    return bool(int(value))


def parse_or_default(value, default_value, parser):
    if value is None or value == '':
        return default_value
    return parser(value)


def parse_yes_no_unknown(value):
    if value is None or value == 0:
        return None
    if value == 1:
        return True
    elif value == 2:
        return False
    return None
