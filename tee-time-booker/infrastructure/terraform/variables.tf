variable "aws_access_key" {
  type    = string
  default = ""
}

variable "aws_secret_key" {
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


