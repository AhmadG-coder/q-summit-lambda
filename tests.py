import boto3

import pytest as pytest
from lambda_function import DynamoDBManager
from unittest import mock

import json
import unittest

if __name__ == '__main__':
    unittest.main()


class TestLambdaHandler(object):


        # with mock.patch.object(dynamodb_manager.table, 'put_item') as mock_put_item:
        #     mock_put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        #     with mock.patch.object(dynamodb_manager.table, 'get_item') as mock_get_item:
        #         mock_get_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        # response = dynamodb_manager.delete_item(event["body"])
        # mock_put_item.assert_called_once()
        # mock_get_item.assert_called_once()

    def test_valid_add(self):
        item = "task0"
        event = {
            "httpMethod": "POST",
            "body": json.dumps(item)
        }
        dynamodb_manager = DynamoDBManager('my-dynamodb-table')
        response = dynamodb_manager.add_item(event["body"])
        assert response["statusCode"] == 200 and response["body"] == "added item to DynamoDB"

    @pytest.mark.parametrize('item', [f"task{x}" for x in range(10)])
    def test_item_already_in_database(self, item):
        event = {
            "httpMethod": "POST",
            "body": json.dumps(item)
        }
        dynamodb_manager = DynamoDBManager('my-dynamodb-table')
        response = dynamodb_manager.add_item(event["body"])
        response = dynamodb_manager.add_item(event["body"])
        assert response["statusCode"] == 400 and response["body"] == "item already in database"
        dynamodb_manager.delete_item(event["body"])