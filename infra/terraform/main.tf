terraform {
  required_version = ">= 1.5.0"
  required_providers {
    opennebula = {
      source  = "OpenNebula/opennebula"
      version = "~> 1.4"
    }
  }
}

provider "opennebula" {
  endpoint = var.endpoint
  username = var.username
  password = var.password
}

variable "endpoint" {
  type = string
}

variable "username" {
  type = string
}

variable "password" {
  type      = string
  sensitive = true
}

variable "datastore_id" {
  type = number
}

variable "image_url" {
  type    = string
  default = "https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img"
}

variable "bridge" {
  type    = string
  default = "br0"
}

variable "network_start" {
  type = string
}

variable "network_size" {
  type    = number
  default = 8
}

resource "opennebula_image" "guest" {
  name          = "vision-qa-guest"
  datastore_id  = var.datastore_id
  description   = "Guest disk for visual console QA"
  type          = "OS"
  path          = var.image_url
  persistent    = false
  permissions   = "600"
}

resource "opennebula_virtual_network" "lab" {
  name        = "vision-qa-lab"
  permissions = "600"
  bridge      = var.bridge
  dnsservers  = ["8.8.8.8"]
  mtu         = 1500
  ar = [
    {
      type  = "IP4"
      size  = var.network_size
      start = var.network_start
    }
  ]
}

resource "opennebula_template" "console" {
  name   = "vision-qa-console"
  cpu    = 1
  vcpu   = 1
  memory = 2048

  disk {
    image_id = opennebula_image.guest.id
  }

  nic {
    network_id = opennebula_virtual_network.lab.id
  }

  graphics {
    type   = "VNC"
    listen = "0.0.0.0"
  }

  os {
    arch = "x86_64"
  }
}

resource "opennebula_virtual_machine" "target" {
  name        = "vision-qa-target"
  template_id = opennebula_template.console.id
}

output "vm_id" {
  value = opennebula_virtual_machine.target.id
}
