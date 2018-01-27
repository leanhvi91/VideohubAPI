from datetime import datetime
import time


def get_time_label(time_stamp, fmt="%Y-%m-%dT%H:%M:%S"):
    """
    Convert from time's stamp to time's label in format: %Y-%m-%dT%H:%M:%S
    :param time_stamp: timestamp
    :param fmt: Format of the targeting time label
    :return:
    """
    utc = datetime.fromtimestamp(time_stamp)
    return time.strftime(fmt, utc.timetuple())


def get_time_stamp(time_label, fmt="%Y-%m-%dT%H:%M:%S"):
    """
    Convert from time label string (%Y-%m-%dT%H:%M:%S) to time stamp
    :param time_label:
    :param fmt: format of the being converted time label
    :return:
    """
    utc = datetime.strptime(time_label, fmt)
    secs = time.mktime(utc.timetuple())
    return int(secs)


if __name__=="__main__":
    lb = get_time_label(1509897600)
    print lb
    secs = get_time_stamp("2017-11-12T00:00:00")
    print secs
    lb = get_time_label(secs)
    print lb