resource "aws_lambda_function" "python_lambda" {
  filename         = "lambda_function.zip"
  function_name    = "python_lambda_function"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_function.handler"
  runtime          = "python3.8"
  timeout          = 10
  memory_size      = 128
}

