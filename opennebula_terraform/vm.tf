resource "opennebula_virtual_machine" "vm1" {
  name = "vm1"
  template_id = opennebula_template.template1.id
}
