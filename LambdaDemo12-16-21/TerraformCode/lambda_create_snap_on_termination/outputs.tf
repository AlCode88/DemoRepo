output "lambda" {
  value = aws_lambda_function.lambda_create_snapshot.qualified_arn
}
