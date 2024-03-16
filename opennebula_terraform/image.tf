resource "opennebula_image" "image1" {
  name = "image1"
  datastore_id = <ID_datastore>
  description = "Disk Image"
  type = "OS"
  path = "http://example.com/ubuntu.qcow2"
  permissions = "600"
}
