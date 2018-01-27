from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from botocore.exceptions import ClientError
import time

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1',
                          endpoint_url="https://dynamodb.ap-southeast-1.amazonaws.com")


def put_item(item, table):
    """

    :param item: Item object
    :param table: Table name
    :return:
    """
    __table = dynamodb.Table(table)

    response = __table.put_item(
        Item=item
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

def batch_put_items(items, table):
    """

    :param items: list of item to be put to dynamodb
    :param table: table name
    :return:
    """
    __table = dynamodb.Table(table)

    with __table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)




def get_item(key, table):
    """
    Get an item
    :param key: primary key / global secondary key
    :param table: table's name
    :return: key matched item
    """
    __table = dynamodb.Table(table)
    try:
        response = __table.get_item(Key=key)
    except ClientError as e:
        err = e.response['Error']['Message']
        print(err)
        return err
    else:
        item = response['Item']
        # print("GetItem succeeded:")
        # print(json.dumps(item, indent=4, cls=DecimalEncoder))
        return item


def delete_item(key, table):
    """
    Delete an item
    :param key: Key object
    :param table: Table name
    :return:
    """
    print("Attempting a conditional delete...")
    __table = dynamodb.Table(table)
    try:
        response = __table.delete_item(Key=key)
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        print("DeleteItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))

MIN_DATE = 0
MAX_DATE = 32503662063
MAX_ITEMS = 100

def list_videos(channelId, fromDate=MIN_DATE, toDate= MAX_DATE, limit=MAX_ITEMS, startKey=None):
    """

    :return:
    """
    print("List videos")
    __table = dynamodb.Table("Videos")
    if startKey:
        response = __table.query(
            IndexName="ChannelId-PublishedAt-index",
            Limit=min(limit, MAX_ITEMS),
            KeyConditionExpression="ChannelId = :v1 AND PublishedAt BETWEEN :v2a AND :v2b",
            ExpressionAttributeValues={
                ":v1": channelId,
                ":v2a": fromDate,
                ":v2b": toDate
            },
            ExclusiveStartKey=startKey,
            ScanIndexForward=False
        )
    else:
        response = __table.query(
            IndexName="ChannelId-PublishedAt-index",
            Limit=min(limit, MAX_ITEMS),
            KeyConditionExpression="ChannelId = :v1 AND PublishedAt BETWEEN :v2a AND :v2b",
            ExpressionAttributeValues={
                ":v1": channelId,
                ":v2a": fromDate,
                ":v2b": toDate
            },
            ScanIndexForward=False
        )

    return response

def list_videos_by_date(channelId, Y1=1970, M1=1, D1=1, Y2=3000, M2=1, D2=1, limit=MAX_ITEMS, startKey=None):
    """

    :param channelId:
    :param Y1:
    :param M1:
    :param D1:
    :param Y2:
    :param M2:
    :param D2:
    :return:
    """
    fromDate = int(time.mktime([Y1, M1, D1, 0, 0, 0, 0, 0, 0]))
    toDate =  int(time.mktime([Y2, M2, D2, 0, 0, 0, 0, 0, 0]))
    return list_videos(channelId=channelId, fromDate=fromDate, toDate=toDate, limit=limit, startKey=startKey)


def list_channels():
    """
    List all channels
    :return:
    """
    print("List channels")
    __table = dynamodb.Table("Channels")
    response = __table.query(
        KeyConditionExpression="RootKey = :v",
        ExpressionAttributeValues={
            ":v": "root"
        }
    )
    return response


if __name__ == "__main__":
    # item = {
    #     'VideoId': "video_18",
    #     'ChannelId': "channel_07",
    #     'PublishedAt': 1920112
    # }
    # put_item(item=item, table="Videos")

    # key = {
    #     'VideoId': "video_18"
    # }
    # get_item(key=key, table="Videos")
    # delete_item(key=key, table="Videos")

    #
    # items = []
    #
    # for i in range(200):
    #     video_id = i
    #     channel_id = i % 10
    #     day = i % 29 + 1
    #     published_at = int(datetime.datetime(2018, 1, day).timestamp())
    #     item = {
    #         "VideoId": ("video_%s" % video_id),
    #         "ChannelId":("channel_%s" % channel_id),
    #         "PublishedAt": published_at
    #     }
    #     items.append(item)
    #
    # batch_put_items(items=items, table="Videos")

    # start_key = {
    #     "ChannelId": "UCwmZiChSryoWQCZMIQezgTg",
    #     "VideoId": "3uw0_HT8vVw",
    #     "PublishedAt": 1242664595
    #   }
    #
    # res = list_videos_by_date(channelId="UCwmZiChSryoWQCZMIQezgTg", maxItems=10, startKey=start_key)
    #
    # txt = json.dumps(res, indent=2, cls=DecimalEncoder)

    res = list_channels()
    txt = json.dumps(res, indent=2, cls=DecimalEncoder)

    print(txt)