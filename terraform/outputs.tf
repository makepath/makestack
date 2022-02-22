output "cluster_egress_ip" {
  value = data.azurerm_public_ip.public-ip.ip_address
}

output "login_server" {
  value = "${azurerm_container_registry.registry.login_server}"
}