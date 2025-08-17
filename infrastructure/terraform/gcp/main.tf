# GCP credentials are sourced from the environment via GOOGLE_APPLICATION_CREDENTIALS

variable "project" {
  description = "GCP project ID"
  type        = string
  validation {
    condition     = length(var.project) > 0
    error_message = "project must not be empty."
  }
}

variable "region" {
  description = "GCP region"
  type        = string
  validation {
    condition     = length(var.region) > 0
    error_message = "region must not be empty."
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_container_cluster" "archon" {
  name     = "${var.project}-archon"
  location = var.region
}

