import json

import pytest as pytest

from lambda_function import lambda_handler, validate_input
from mockito import mock, when, verify
from botocore.exceptions import ClientError

class TestLambdaHandler:
    def test_valid_input(self):
        event = {
            "httpMethod": "POST",
            "body": json.dumps({"item": "task_name"})
        }

        dynamodb_client_mock = mock()
        when(dynamodb_client_mock).put_item(TableName="my-dynamodb-table", Item={"name": {"S": "task_name"}}).thenReturn(None)

        response = lambda_handler(event, {})
        assert response['statusCode'] == 200
        assert response['body'] == 'Item added to DynamoDB table'

        verify(dynamodb_client_mock).put_item(TableName="my-dynamodb-table", Item={"name": {"S": "task_name"}})

    def test_invalid_input(self):
        event = {
            "httpMethod": "POST",
            "body": json.dumps({"item": 123})
        }

        response = lambda_handler(event, {})
        assert response['statusCode'] == 400
        assert response['body'] == 'Invalid item name provided'

    # Other test methods...


class TestInputValidation:
    @pytest.mark.parametrize("item_name", ["task_name", "another_task", "123"])
    def test_valid_input(self, item_name):
        event = {
            "httpMethod": "POST",
            "body": {"item": item_name}
        }

        result = validate_input(event["body"])
        assert result is True

    @pytest.mark.parametrize("item_name", [None, 123, True, {"item": "task_name"}])
    def test_invalid_input(self, item_name):
        event = {
            "httpMethod": "POST",
            "body": item_name
        }

        result = validate_input(event)
        assert result is False