resource "opennebula_template" "template1" {
  name = "template1"
  cpu = 1
  vcpu = 1
  memory = 2048
  disk {
    image_id = opennebula_image.image1.id
  }
  nic {
    network_id = opennebula_virtual_network.vnet1.id
  }
  graphics {
    type = "VNC"
    listen = "0.0.0.0"
  }
  os {
    arch = "x86_64"
  }
}
