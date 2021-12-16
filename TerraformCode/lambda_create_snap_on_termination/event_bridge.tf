# ==================  Event Based Rules ==========================
resource "aws_cloudwatch_event_rule" "event_based_triggering_on_termination" {
    name = "Trigger_Lambda_on_termination"
    description = "Trigger_Lambda on EC2 terminatio"
    event_pattern  = <<EOF
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["terminated"]
  }
}
EOF
}

# =================== Event Based Target ==============================
resource "aws_cloudwatch_event_target" "based_on_event" {
    rule = aws_cloudwatch_event_rule.event_based_triggering_on_termination.name
    target_id = "lambda_create_snapshot"
    arn = aws_lambda_function.lambda_create_snapshot.arn
}

# ================== Lambda Permission ================================
resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda_create_snapshot.function_name # Define your Lambda Function
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.event_based_triggering_on_termination.arn
}