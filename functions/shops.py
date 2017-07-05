import json
import os
import boto3


def __parse_shops(event):
    shops = []
    payload = event
    if payload['data']:
        for shop in payload['data']:
            if shop['type'] == 'shop':
                attrs = shop['attributes']
                shops.append({"name": str(attrs['name']), "shop_number": int(attrs['shop_number'])})
    return shops


def __save_shops(shops):
    table = get_shops_table()

    for shop in shops:
        result = table.put_item(
            Item={
                'shopNumber': shop['shop_number'],
                'name': shop['name']
            }
        )


def get_shops_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_SHOPS_TABLE'])
    return table


def upload_shops(event, context):
    """Upload the list of shops."""

    shops = __parse_shops(event)
    __save_shops(shops)

    body = {
        "message": "Shops uploaded (count=%d)" % len(shops),
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def list_shops(event, context):
    """Get the list of shops"""
    table = get_shops_table()
    shops = [{"shop_number": int(item['shopNumber']), "name": str(item['name'])}
             for item in table.scan()['Items']]
    body = {
        'data': [
            [{
                "type": 'shop',
                "id": shop['shop_number'],
                "attributes": {
                    "name": shop['name']
                }
            }
            for shop in shops]
        ]
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
