import json
import os
import boto3
import datetime


def __parse_daily_sales(event):
    shops = []
    payload = event
    if payload['data']:
        for shop in payload['data']:
            if shop['type'] == 'daily-sales':
                attrs = shop['attributes']
                shops.append({
                    "shop_number": int(attrs['shop_number']),
                    "date": datetime.datetime.strptime(attrs['date'], '%Y-%m-%d').date(),
                    "sales": int(attrs['sales'])
                })
    return shops


def __save_sales(daily_sales):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_SALES_TABLE'])

    for day in daily_sales:
        result = table.put_item(
            Item={
                'shopNumber': day['shop_number'],
                'date': day['date'].isoformat(),
                'sales': day['sales']
            }
        )


def upload_sales(event, context):
    """Upload a list of daily sales."""

    sales = __parse_daily_sales(event)
    __save_sales(sales)

    body = {
        "message": "Sales data uploaded (count=%d)" % len(sales),
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
