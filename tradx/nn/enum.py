import datetime

def timedelta_to_str(td:datetime.timedelta):
    if td == datetime.timedelta(seconds=60):
        return "1m"
    if td == datetime.timedelta(days=1):
        return "1d"