# AWS credentials are sourced from the environment:
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  validation {
    condition     = length(var.cluster_name) >= 3 && length(var.cluster_name) <= 30
    error_message = "cluster_name must be 3-30 characters."
  }
}

variable "region" {
  description = "AWS region"
  type        = string
  validation {
    condition     = can(regex("^([a-z]{2}-){2}[0-9]$", var.region))
    error_message = "region must match pattern e.g. us-west-2."
  }
}

variable "cluster_role_arn" {
  description = "IAM role ARN for EKS cluster"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
  validation {
    condition     = length(var.subnet_ids) > 0
    error_message = "At least one subnet ID must be provided."
  }
}

provider "aws" {
  region = var.region
}

resource "aws_eks_cluster" "archon" {
  name     = var.cluster_name
  role_arn = var.cluster_role_arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

