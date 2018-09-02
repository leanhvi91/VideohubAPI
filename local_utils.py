from datetime import datetime
import time
import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    """
    Helper class to convert a DynamoDB item to JSON.
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def wrap_response(body):
    """
    Wrap the response
    :param body:
    :return:
    """
    response = {
        "statusCode": 200,
        "headers": {
             "Access-Control-Allow-Origin": "*",
             "Access-Control-Allow-Credentials": "true"
        },
        "body": json.dumps(body, indent=2, cls=DecimalEncoder, ensure_ascii=False)
    }

    return response

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

