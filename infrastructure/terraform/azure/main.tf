# Azure credentials are sourced from the environment: ARM_CLIENT_ID, ARM_CLIENT_SECRET, ARM_TENANT_ID

variable "resource_group_name" {
  description = "Azure resource group"
  type        = string
  validation {
    condition     = length(var.resource_group_name) > 0
    error_message = "resource_group_name must not be empty."
  }
}

variable "location" {
  description = "Azure region"
  type        = string
  validation {
    condition     = length(var.location) > 0
    error_message = "location must not be empty."
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_kubernetes_cluster" "archon" {
  name                = "archon-cluster"
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = "archon"
}

