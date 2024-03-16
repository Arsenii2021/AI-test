terraform {
  required_providers {
    opennebula = {
      source = "OpenNebula/opennebula"
      version = "<версия_terraform>"
    }
  }
}

provider "opennebula" {
  endpoint = "http://<адрес_сервера>:<порт>/RPC2"
  username = "<имя_пользователя>"
  password = "<пароль>"
}
