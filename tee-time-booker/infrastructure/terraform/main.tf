# Define the Lambda function
resource "aws_lambda_function" "brs_booking_lambda" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "lambda-TeeBooker-${var.environment}-${var.short_region}"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "tee_time_booker.lambda_handler"
  runtime       = "python3.8"
  timeout       = 60

  environment {
    variables = local.lambda_event_payload
  }

  tags = local.tags
  }

# Define the IAM role for the Lambda function
resource "aws_iam_role" "lambda_exec" {
  name = "brs_booking_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_exec" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_exec.name
}

# Define the CloudWatch Event Rule for the Lambda function
resource "aws_cloudwatch_event_rule" "schedule_rule_1" {
  name                = "golf_wednesdays_schedule_rule"
  description         = "Schedule rule for the BRS Booking Lambda function"
  schedule_expression = var.function_schedule

  tags = local.tags
}

resource "aws_cloudwatch_event_rule" "schedule_rule_2" {
  name                = "brs_booking_schedule_rule"
  description         = "Schedule rule for the BRS Booking Lambda function"
  schedule_expression = "cron(57 11 28 JUL ? 2023)"

  tags = local.tags
}

# Define the CloudWatch Event Target for the Lambda function
resource "aws_cloudwatch_event_target" "lambda_target_1" {
  rule      = aws_cloudwatch_event_rule.schedule_rule_1.name
  target_id = "brs_booking_lambda_target"
  arn       = aws_lambda_function.brs_booking_lambda.arn
}

resource "aws_cloudwatch_event_target" "lambda_target_2" {
  rule      = aws_cloudwatch_event_rule.schedule_rule_2.name
  target_id = "brs_booking_lambda_target"
  arn       = aws_lambda_function.brs_booking_lambda.arn
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../../bin"
  output_path = "../../lambda_main.zip"
}
