terraform {
required_version    = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.42.0"
    }
  }
}

provider "openstack" {
  alias = "ovh"
}

# Creating an SSH key pair resource
resource "openstack_compute_keypair_v2" "admin_keypair" {
  provider   = openstack.ovh
  name       = "admin_keypair"
  public_key = file("~/.ssh/id_ed25519.pub")
}

# Creating the instance
resource "openstack_compute_instance_v2" "nginx" {
  name        = "terraform_instance"
  provider    = openstack.ovh
  image_name  = "Debian 12"
  flavor_name = "d2-4"
  key_pair    = openstack_compute_keypair_v2.admin_keypair.name

  user_data = <<EOF
#cloud-config
package_upgrade: true
packages:
  - nginx
EOF

  network {
    name      = "Ext-Net"
  }
}

output "nginx_ip" {
  value = openstack_compute_instance_v2.nginx.access_ip_v4
}
