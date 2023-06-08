import boto3

import pytest as pytest
from lambda_function import lambda_handler, validate_input, DynamoDBManager
from unittest import mock

import json
import unittest
from unittest.mock import MagicMock


class TestLambdaHandlerDlete(unittest.TestCase):

    def test_delete_item_success(self):
        # Mock the event and context objects for the DELETE request
        event = {
            "httpMethod": "DELETE",
            "body": json.dumps({"item": "example_item"})
        }
        # context = MagicMock()

        # Call the lambda_handler function
        response = lambda_handler(event, {})

        # Verify the response
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["body"], "Item deleted from DynamoDB")

    def test_delete_item_invalid_name(self):
        # Mock the event and context objects for the DELETE request with an invalid item name
        event = {
            "httpMethod": "DELETE",
            "body": json.dumps({"item": 123})  # Invalid item name, should be a string
        }
        context = MagicMock()

        # Call the lambda_handler function
        response = lambda_handler(event, context)

        # Verify the response
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["body"], "Invalid item name provided")

    def test_delete_item_no_body(self):
        # Mock the event and context objects for the DELETE request with no body
        event = {
            "httpMethod": "DELETE"
        }
        context = MagicMock()

        # Call the lambda_handler function
        response = lambda_handler(event, context)

        # Verify the response
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["body"], "No body found in the request")

    def test_delete_item_invalid_payload(self):
        # Mock the event and context objects for the DELETE request with an invalid JSON payload
        event = {
            "httpMethod": "DELETE",
            "body": "invalid_json_payload"
        }
        context = MagicMock()

        # Call the lambda_handler function
        response = lambda_handler(event, context)

        # Verify the response
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["body"], "Invalid JSON payload")


if __name__ == '__main__':
    unittest.main()


class TestLambdaHandler(object):

    @pytest.fixture(autouse=True)
    def setUp(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('my-dynamodb-table')
        yield

    def test_valid_add(self):
        item = "task0"
        event = {
            "httpMethod": "POST",
            "body": json.dumps(item)
        }
        dynamodb_manager = DynamoDBManager('my-dynamodb-table')

        with mock.patch.object(dynamodb_manager.table, 'put_item') as mock_get_item:
            # Configure the return value of the mocked method
            mock_get_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
            # Call the put_item method
            response = dynamodb_manager.add_item(event["body"])
            assert response["statusCode"] == 200 and response["body"] == "added item to DynamoDB"

    @pytest.mark.parametrize('item', [f"task{x}" for x in range(10)])
    def test_item_already_in_database(self, item):
        event = {
            "httpMethod": "POST",
            "body": json.dumps(item)
        }
        dynamodb_manager = DynamoDBManager('my-dynamodb-table')

        with mock.patch.object(dynamodb_manager.table, 'get_item') as mock_get_item:
            # Configure the return value of the mocked method
            mock_get_item.return_value = {'Item': {"name": item}, 'ResponseMetadata': {'HTTPStatusCode': 200}}
            # Call the put_item method
            response = dynamodb_manager.add_item(event["body"])
            assert response["statusCode"] == 400 and response["body"] == "item already in database"
            # Check the response

    def test_get_valid_input(self):
        dynamodb_manager = DynamoDBManager('my-dynamodb-table')

        with mock.patch.object(dynamodb_manager.table, 'scan') as mock_put_item:
            # Configure the return value of the mocked method
            mock_put_item.return_value = {'Items': [{'name': '{"item": "task0"}'}, {'name': 'task0'}, {'name': 'ane1m'}, {'name': 'anem'}], 'Count': 4, 'ScannedCount': 4, 'ResponseMetadata': {'HTTPStatusCode': 200}}
            response = dynamodb_manager.list_items()
            assert response == '{"item": "task0"}\ntask0\nane1m\nanem\n'
        # Check the response

    def test_invalid_input(self):
        event = {
            "httpMethod": "POST",
            "body": json.dumps({"item": 123})
        }

        response = lambda_handler(event, {})
        assert response['statusCode'] == 400
        assert response['body'] == 'Invalid item name provided'

    # Other test methods...