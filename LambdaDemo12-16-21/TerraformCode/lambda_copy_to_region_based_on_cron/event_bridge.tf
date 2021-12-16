#=================== CW Event Rule =================================
resource "aws_cloudwatch_event_rule" "backup_snapshot_reion_cron" {
     name = "backup_snapshot_region"
     description = "Make backup of snapshot to us-east-2"
     schedule_expression = "rate(4 minutes)"
}

#=================== CW Event Target =================================
resource "aws_cloudwatch_event_target" "copy_to_region" {
     rule = aws_cloudwatch_event_rule.backup_snapshot_reion_cron.name
     target_id = "copy-us-east-1"
     arn = aws_lambda_function.lambda_copy_to_region.arn
}

#=================== CW Lambda Permission =================================
resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
     statement_id = "AllowExecutionFromCloudWatch"
     action = "lambda:InvokeFunction"
     function_name = aws_lambda_function.lambda_copy_to_region.function_name
     principal = "events.amazonaws.com"
     source_arn = aws_cloudwatch_event_rule.backup_snapshot_reion_cron.arn
}