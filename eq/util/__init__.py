from datetime import datetime

def ts_to_dt(string):
    "Converts a timestamp to a datetime. Returns None if failed"
    if not string.isdigit():
        return None

    integer = int(string)

    return datetime.fromtimestamp(integer)
