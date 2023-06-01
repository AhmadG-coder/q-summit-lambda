import json
import os

import boto3


def validate_input(body):
    if "item" in body and isinstance(body["item"], str):
        return True
    return False


class DynamoDBManager:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        os.environ["AWS_REGION"] = "us-east-1"
        self.table_name = table_name
        self.table = self.dynamodb.Table(table_name)

    def add_item(self, item):
        item = str(item)
        item_data = {
            'name': item
        }
        response = self.table.put_item(Item=item_data)
        return "Item added to DynamoDB table:", item

    def delete_item(self, item):
        # Convert the item to a string if needed
        item_name = str(item)

        # Delete the item from DynamoDB
        response = self.table.delete_item(Key={'name': item_name})

        return response

    def list_items(self):
        response = self.table.scan()
        items = response.get('Items', [])
        print("Listing items:")
        printing_str = ""
        for item in items:
            printing_str += item['name'] + "\n"
            print(item['name'])
        return printing_str


def lambda_handler(event, context):
    if event["httpMethod"] == "POST":
        if "body" in event:
            try:
                body = json.loads(event["body"])
                if validate_input(body):
                    dynamodb_manager = DynamoDBManager('my-dynamodb-table')
                    response = dynamodb_manager.add_item(body["item"])
                    return {
                        'statusCode': 200,
                        'body': "added item to DynamoDB"
                    }
                else:
                    return {
                        'statusCode': 400,
                        'body': 'Invalid item name provided'
                    }
            except ValueError:
                return {
                    'statusCode': 400,
                    'body': 'Invalid JSON payload'
                }
        else:
            return {
                'statusCode': 400,
                'body': 'No body found in the request'
            }
    elif event["httpMethod"] == "GET":
        dynamodb_manager = DynamoDBManager('my-dynamodb-table')
        response = dynamodb_manager.list_items()
        return {
            'statusCode': 200,
            'body': response
        }
    elif event["httpMethod"] == "DELETE":
        if "body" in event:
            try:
                body = json.loads(event["body"])
                if validate_input(body):
                    dynamodb_manager = DynamoDBManager('my-dynamodb-table')
                    response = dynamodb_manager.delete_item(body["item"])
                    return {
                        'statusCode': 200,
                        'body': "Item deleted from DynamoDB"
                    }
                else:
                    return {
                        'statusCode': 400,
                        'body': 'Invalid item name provided'
                    }
            except ValueError:
                return {
                    'statusCode': 400,
                    'body': 'Invalid JSON payload'
                }
        else:
            return {
                'statusCode': 400,
                'body': 'No body found in the request'
            }
    else:
        return {
            'statusCode': 400,
            'body': 'Invalid request method'
        }