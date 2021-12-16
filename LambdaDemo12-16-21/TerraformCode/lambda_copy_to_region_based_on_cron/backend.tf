terraform {
  backend "s3" {
    bucket = "terraform-bucket-tb"
    key    = "Resources/lambda_copy_backup_cron.tfstate"
    region = "us-east-1"
    # dynamodb_table = "terraform-state-locks"
  }
}
