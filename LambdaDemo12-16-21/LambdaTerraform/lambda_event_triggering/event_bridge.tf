# ==================  Event Based Rules ==========================
resource "aws_cloudwatch_event_rule" "event_based_triggering" {
    name = "Start_the_instance_based_on_condition"
    description = "Starts Instance Based On State"
    event_pattern  = <<EOF
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["stopped"]
  }
}
EOF
}

# =================== Event Based Target ==============================
resource "aws_cloudwatch_event_target" "based_on_event" {
    rule = aws_cloudwatch_event_rule.event_based_triggering.name
    target_id = "check_foo"
    arn = aws_lambda_function.lambda.arn
}

# ================== Lambda Permission ================================
resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda.function_name # Define your Lambda Function
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.event_based_triggering.arn
}