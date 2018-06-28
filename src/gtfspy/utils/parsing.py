def str_to_bool(value):
    return bool(int(value))

def parse_or_default(value, default_value, parser):
    if value is None or value == '':
        return default_value
    return parser(value)
