################ Custom Policy #####################################
resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_policy_event"
  description = "A test policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["*"],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

################### Policy Attachment to Role #########################
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment_event" {
  role       = aws_iam_role.iam_for_lambda_start.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}