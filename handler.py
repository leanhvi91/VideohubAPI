import dynamo_crud as db
import serializer
from local_utils import get_time_stamp, wrap_response



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
    return wrap_response(body)


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
    return wrap_response(video)


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

            if "fromDate" in param:
                from_date = get_time_stamp(param["fromDate"])
            else:
                from_date = None

            if "toDate" in param:
                to_date = get_time_stamp(param["toDate"])
            else:
                to_date = None

            from_db = db.list_videos(channelId=channelId, limit=limit, startKey=start_key, fromDate=from_date, toDate=to_date)

            to_client = {
                "videos": from_db["Items"]
            }

            if "LastEvaluatedKey" in from_db:
                next_key = serializer.serialize(from_db["LastEvaluatedKey"])
                to_client["nextToken"] = next_key

            return wrap_response(to_client)
    else:
        return wrap_response(None)


def list_channels(event, context):
    """

    :param event:
    :param context:
    :return:
    """
    from_db = db.list_channels()
    to_client ={
        "channels": from_db["Items"]
    }
    return wrap_response(to_client)


