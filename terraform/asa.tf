resource "azurerm_storage_account" "storage-account" {
  name                     = "${var.prefix}storageaccount"
  resource_group_name      = azurerm_resource_group.resource-group.name
  location                 = azurerm_resource_group.resource-group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  enable_https_traffic_only = true
  allow_blob_public_access  = true
  blob_properties{
    cors_rule{
        allowed_headers = ["*"]
        allowed_methods = ["GET","HEAD","POST","PUT"]
        allowed_origins = ["*"]
        exposed_headers = ["*"]
        max_age_in_seconds = 0
        }
    }
}

resource "azurerm_storage_container" "storage-container" {
  name                  = "static"
  storage_account_name  = azurerm_storage_account.storage-account.name
  container_access_type = "blob"
}
