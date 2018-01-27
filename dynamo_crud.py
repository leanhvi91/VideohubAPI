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


def list_videos(channelId, fromDate=None, toDate= None, limit=20, startKey=None):
    # type: (str, str, str, int, str) -> object
    """

    :return:
    """
    print("List videos")
    __table = dynamodb.Table("Videos")

    key_condition_expression = "ChannelId = :v1"
    expression_attribute_values = {
        ":v1": channelId
    }

    if fromDate and toDate:
        key_condition_expression += " AND PublishedAt BETWEEN :v2 AND :v3"
        expression_attribute_values[":v2"] = fromDate
        expression_attribute_values[":v3"] = toDate
    else:
        if fromDate:
            key_condition_expression += " AND PublishedAt >= :v2"
            expression_attribute_values[":v2"] = fromDate
        elif toDate:
            key_condition_expression += " AND PublishedAt <= :v3"
            expression_attribute_values[":v3"] = toDate

    if startKey:
        response = __table.query(
            IndexName="ChannelId-PublishedAt-index",
            Limit=min(limit, 100),
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExclusiveStartKey=startKey,
            ScanIndexForward=False
        )
    else:
        response = __table.query(
            IndexName="ChannelId-PublishedAt-index",
            Limit=min(limit, 100),
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ScanIndexForward=False
        )

    return response


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

    res = list_videos(channelId="UCzWQYUVCpZqtN93H8RR44Qw", fromDate=None, toDate=1413166406, limit=5)
    txt = json.dumps(res, indent=2, cls=DecimalEncoder)

    print(txt)