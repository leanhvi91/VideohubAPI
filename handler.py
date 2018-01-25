import json
import dynamo_crud as db
import decimal
import serializer


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


def response(body):
    """
    Wrap the response
    :param body:
    :return:
    """
    response = {
        "statusCode": 200,
        "body": json.dumps(body, indent=2, cls=DecimalEncoder)
    }

    return response


def hello(event, context):
    """

    :param event:
    :param context:
    :return:
    """
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    return response(body)


def get_video(event, context):
    """
    Return list videos
    :return:
    """
    table = "Videos"
    key = {
        'VideoId': "3uw0_HT8vVw"
    }
    video = db.get_item(key=key, table=table)
    return response(video)


def list_videos(event, context):
    """
    Return list videos
    :return:
    """
    if "queryStringParameters" in event:
        if "channelId" in event["queryStringParameters"]:
            channelId = event["queryStringParameters"]["channelId"]
            if "startKey" in event:
                start_key = serializer.deserialize(event["startKey"])
            else:
                start_key = None
            videos = db.list_videos_by_date(channelId=channelId, maxItems=50, startKey=start_key)
            if "LastEvaluatedKey" in videos:
                next_key = serializer.serialize(videos["LastEvaluatedKey"])
                videos["nextKey"] = next_key

            return response(videos)
    else:
        return response(None)


def list_channels(event, context):
    """

    :param event:
    :param context:
    :return:
    """
    channels = db.list_channels()
    return response(channels)