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
        "headers": {
             "Access-Control-Allow-Origin": "*",
             "Access-Control-Allow-Credentials": "true"
        },
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
        param = event["queryStringParameters"]
        if "channelId" in param:
            channelId = param["channelId"]
            if "pageToken" in param:
                start_key = serializer.deserialize(param["pageToken"])
            else:
                start_key = None
            if "limit" in param:
                limit = int(param["limit"])
            else:
                limit = 20
            videos = db.list_videos_by_date(channelId=channelId, limit=limit, startKey=start_key)
            if "LastEvaluatedKey" in videos:
                next_key = serializer.serialize(videos["LastEvaluatedKey"])
                videos["NextToken"] = next_key

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