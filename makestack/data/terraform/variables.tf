variable "prefix" {
  description = "A prefix used for all resources"
  default     = "makestack"
}

variable "location" {
  description = "The Azure Region in which all resources should be provisioned"
  default     = "East US"
}