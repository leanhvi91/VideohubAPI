import json
import decimal
from urllib import quote, unquote

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

def serialize(obj):
    """
    Serialize object to string
    :param obj:
    :return:
    """
    s = json.dumps(obj, cls=DecimalEncoder)
    return quote(s)

def deserialize(code):
    """
    Deserialize string to object
    :param code:
    :return:
    """
    s = unquote(code)
    return json.loads(s)
