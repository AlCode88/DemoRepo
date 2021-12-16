################ Custom Policy #####################################
resource "aws_iam_policy" "lambda_policy_copy_to_region" {
  name        = "lambda_policy_copy_to_region"
  description = "Lambda policy copy to region"

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
  role       = aws_iam_role.iam_for_lambda_stop.name
  policy_arn = aws_iam_policy.lambda_policy_copy_to_region.arn
}