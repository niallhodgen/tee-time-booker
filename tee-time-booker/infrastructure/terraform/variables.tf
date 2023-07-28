variable "AWS_ACCESS_KEY" {
  type    = string
  default = ""
}

variable "AWS_SECRET_KEY" {
  type    = string
  default = ""
}

variable "environment" {
  type        = string
  description = "Environment, e.g., Dev, Stage or Prod"
}

variable "region" {
  type        = string
  description = "Subscription resource location, e.g. South Central US, East US 2, etc."
}

variable "short_region" {
  type        = string
  description = "Abbreviation of subscription resources location, e.g. scus, east2, etc."
}

variable "function_schedule" {
  description = "The schedule expression for the Lambda function"
  type        = string
  default     = "cron(59 19 ? JUL,AUG,SEP 4/7 2023)" # Each Wednesday in August, July and September 2023 @ 19:59:55
}

