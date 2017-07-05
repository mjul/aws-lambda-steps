import json
import os
import boto3
from boto3.dynamodb.conditions import Key

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
                    "date": parse_iso_date_string(attrs['date']),
                    "sales": int(attrs['sales'])
                })
    return shops


def parse_iso_date_string(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d').date()


def __save_sales(daily_sales):
    table = __get_sales_table()

    for day in daily_sales:
        result = table.put_item(
            Item={
                'shopNumber': day['shop_number'],
                'date': day['date'].isoformat(),
                'sales': day['sales']
            }
        )


def __get_sales_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_SALES_TABLE'])
    return table


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


def generate_weekly_report(event, context):
    """Create a weekly report for sales."""

    today = parse_iso_date_string(event['date'])
    shop_number = int(event['shopNumber'])

    one_week_ago = datetime.date.fromordinal(today.toordinal() - 7)

    # DynamoDB has only limited query capabilities, so this is a bit clunky
    table = __get_sales_table()
    last_week_sales = []

    response = table.query(
        KeyConditionExpression=Key('shopNumber').eq(shop_number) & Key('date').gt(one_week_ago.isoformat()))

    for item in response['Items']:
        last_week_sales.append({
            'shop_number': int(item['shopNumber']),
            'date': parse_iso_date_string(item['date']),
            'sales': int(item['sales'])
        })

    body = {
        "message": "Sales report generated",
        "input": event,
        "data": [{"date": s['date'].isoformat(), "sales": s['sales'], "shopNumber": s['shop_number']}
                 for s in last_week_sales]
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
