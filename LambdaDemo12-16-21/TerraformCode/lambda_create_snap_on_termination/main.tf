data "archive_file" "zip" {
  type        = "zip"
  source_file = "hello_lambda.py"
  output_path = "hello_lambda.zip"
}

########### Assume Role Policy ###############################
data "aws_iam_policy_document" "policy" {
  statement {
    sid    = ""
    effect = "Allow"

    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

############ IAM Role for Lambda ##############################
resource "aws_iam_role" "iam_for_lambda_create_snapshot" {
  name               = "Create_Snap_On_Temination"
  assume_role_policy = data.aws_iam_policy_document.policy.json
}

################ Lambda Resource ###############################
resource "aws_lambda_function" "lambda_create_snapshot" {
  function_name = "CreateSnapshotOnTermination"

  filename         = data.archive_file.zip.output_path
  source_code_hash = data.archive_file.zip.output_base64sha256
  
  role    = aws_iam_role.iam_for_lambda_create_snapshot.arn
  handler = "hello_lambda.lambda_handler"
  runtime = "python3.6"
  timeout = 400

  environment {
    variables = {
      greeting = "Hello"
    }
  }
}