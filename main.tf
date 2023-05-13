provider "aws" {
  region = "us-east-1"  # Set your desired AWS region
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "my-lambda-function"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  timeout       = 10
  role          = aws_iam_role.lambda_execution.arn

  // Include the path to your lambda_function.py file
  filename         = "lambda_function.zip"
  source_code_hash = filebase64sha256("lambda_function.zip")
  depends_on = [data.archive_file.lambdazip]
}

resource "aws_cloudwatch_log_group" "my_log_group" {
  name = "/aws/lambda/my-lambda-function"
}


data "archive_file" "lambdazip" {
  type        = "zip"
  output_path = "lambda_function.zip"
  source_file = "lambda_function.py"
}


resource "aws_iam_policy" "dynamodb_access" {
  name        = "dynamodb-access-policy"
  description = "Allows access to DynamoDB"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:DeleteItem",
        "dynamodb:Scan",
        "dynamodb:Query",
        "dynamodb:UpdateItem"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/${aws_dynamodb_table.my_table.name}"
    }
  ]
}
EOF
}


resource "aws_apigatewayv2_route" "delete_route" {
  api_id    = aws_apigatewayv2_api.my_api.id
  route_key = "DELETE /"

  target = "integrations/${aws_apigatewayv2_integration.delete_integration.id}"
}

resource "aws_apigatewayv2_integration" "delete_integration" {
  api_id             = aws_apigatewayv2_api.my_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.my_lambda.invoke_arn
  passthrough_behavior = "WHEN_NO_MATCH"

}

resource "aws_dynamodb_table" "my_table" {
  name           = "my-dynamodb-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "name"

  attribute {
    name = "name"
    type = "S"
  }
  point_in_time_recovery {
    enabled = false
  }
}


resource "aws_iam_role_policy_attachment" "lambda_execution_policy_attachment" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = aws_iam_policy.dynamodb_access.arn
}

resource "aws_iam_role" "lambda_execution" {
  name = "lambda-execution-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [

    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_execution" {
  name       = "lambda-execution-policy-attachment"
  roles      = [aws_iam_role.lambda_execution.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_permission" "api_gateway_invoke_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = aws_apigatewayv2_api.my_api.arn
}


resource "aws_apigatewayv2_api" "my_api" {
  name          = "my-api"
  protocol_type = "HTTP"

}

resource "aws_apigatewayv2_integration" "my_integration" {
  api_id             = aws_apigatewayv2_api.my_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.my_lambda.invoke_arn
  passthrough_behavior = "WHEN_NO_MATCH"

}


resource "aws_apigatewayv2_route" "my_route" {
  api_id    = aws_apigatewayv2_api.my_api.id
  route_key = "POST /"

  target = "integrations/${aws_apigatewayv2_integration.my_integration.id}"
}

resource "aws_apigatewayv2_stage" "my_stage" {
  api_id      = aws_apigatewayv2_api.my_api.id
  name        = "prod"
  auto_deploy = false

  default_route_settings {
    logging_level            = "INFO"
    data_trace_enabled       = true
    detailed_metrics_enabled = true
    throttling_burst_limit   = 5000
    throttling_rate_limit    = 10000
  }
}

resource "aws_apigatewayv2_deployment" "my_deployment" {
  api_id      = aws_apigatewayv2_api.my_api.id
  description = "Deployment for my API"
  depends_on  = [aws_apigatewayv2_route.my_route]
}


output "api_endpoint" {
  value = aws_apigatewayv2_api.my_api.api_endpoint
}

