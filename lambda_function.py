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
            'name': item.replace('\"', "")
        }
        response = self.table.get_item(Key=item_data)
        if 'Item' in response:
            print("Item already exists in DynamoDB table:", item)
            return compose_return(status_code=400, message="item already in database")
        response = self.table.put_item(Item=item_data)["ResponseMetadata"]["HTTPStatusCode"]
        if response == 200:
            body = "added item to DynamoDB"
        return compose_return(status_code=response, message=body)

    def delete_item(self, item):
        # Convert the item to a string if needed
        item_name = str(item.replace('\"', ""))

        # Delete the item from DynamoDB
        response = self.table.delete_item(Key={'name': item_name})

        return response["ResponseMetadata"]["HTTPStatusCode"]

    def list_items(self):
        response = self.table.scan()
        items = response.get('Items', [])
        print("Listing items:")
        printing_str = ""
        for item in items:
            printing_str += item['name'] + "\n"
            print(item['name'])
        return compose_return(status_code=200, message=printing_str)


def compose_return(status_code, message):
    return {
        'statusCode': status_code,
        'body': message
    }


def lambda_handler(event, context):
    body = json.loads(event["body"])
    if validate_input(body):
        dynamodb_manager = DynamoDBManager('my-dynamodb-table')
    else:
        response = 400
        body = "Invalid item name provided"
        return compose_return(status_code=response,message=body)
    if event["httpMethod"] == "POST":
            try:
                response = dynamodb_manager.add_item(body["item"])
                return response
            except ValueError:
                return compose_return(status_code=400, message="invalid JSON payload")
    elif event["httpMethod"] == "GET":
        response = dynamodb_manager.list_items()
        return response
    elif event["httpMethod"] == "DELETE":
            try:
                response = dynamodb_manager.delete_item(body["item"])
                return response
            except ValueError:
                return compose_return(status_code=400, message="invalid JSON payload")
    else:
        return compose_return()