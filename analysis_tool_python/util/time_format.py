import time
from datetime import datetime, timedelta


def load_time_to_utc_unix(time_str, time_format):
    t = datetime.strptime(time_str.split(' +')[0], time_format)
    if "+0800" in time_str or "CST" in time_str:
        t = t + timedelta(hours=-8)
    return time.mktime(t.timetuple())


def utc_unix_to_date(unix_str):
    if unix_str.startswith("0x"):
        unix_int = int(unix_str, 16)
    else:
        unix_int = int(unix_str)
    t = datetime.fromtimestamp(unix_int)
    return t.strftime("%Y%m%d")
