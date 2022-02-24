output "registry_name" {
  value = "${azurerm_container_registry.registry.name}"
}

output "registry_login_server" {
  value = "${azurerm_container_registry.registry.login_server}"
}

output "registry_admin_username" {
  value = "${azurerm_container_registry.registry.admin_username}"
}

output "registry_admin_password" {
  value = "${azurerm_container_registry.registry.admin_password}"
  sensitive = true
}

output "storage_account_name" {
  value = "${azurerm_storage_account.storage-account.name}"
}

output "storage_account_primary_access_key" {
  value = "${azurerm_storage_account.storage-account.primary_access_key}"
  sensitive = true
}

output "aks_name" {
  value = "${azurerm_kubernetes_cluster.aks.name}"
  sensitive = true
}

output "aks_resource_group_name" {
  value = "${azurerm_kubernetes_cluster.aks.resource_group_name}"
  sensitive = true
}
