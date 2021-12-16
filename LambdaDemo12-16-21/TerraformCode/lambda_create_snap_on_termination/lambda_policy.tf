################ Custom Policy #####################################
resource "aws_iam_policy" "lambda_policy_create_snapshot" {
  name        = "lambda_policy_to_create_snapshot_upon_termination"
  description = "CreateSnapshotOnTermination"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["*"],
      "Resource": "*"
    }
  ]
}
EOF
}

################### Policy Attachment to Role #########################
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment_event" {
  role       = aws_iam_role.iam_for_lambda_create_snapshot.name
  policy_arn = aws_iam_policy.lambda_policy_create_snapshot.arn
}