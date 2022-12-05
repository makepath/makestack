resource "azurerm_container_registry" "registry" {
  name                = "${var.prefix}registry"
  resource_group_name = "${azurerm_resource_group.resource-group.name}"
  location            = "${azurerm_resource_group.resource-group.location}"
  sku                 = "Standard"
  admin_enabled       = true
}
