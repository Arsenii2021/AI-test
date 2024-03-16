resource "opennebula_virtual_network" "vnet1" {
  name = "vnet1"
  permissions = "600"
  bridge = "br0"
  dnsservers = ["8.8.8.8"]
  mtu = 1500
  ar = [
    {
      type        = "IP4"
      size        = 10
      start       = "xxx.xxx.x.x"
    }
  ]
}
