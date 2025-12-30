# 1. RED (VCN)
resource "oci_core_vcn" "mi_red" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = var.compartment_ocid
  display_name   = "Red-SimpleRAG"
}

# 2. PUERTA A INTERNET
resource "oci_core_internet_gateway" "mi_ig" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.mi_red.id
  display_name   = "InternetGateway"
}

# 3. TABLA DE RUTAS
resource "oci_core_route_table" "mi_rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.mi_red.id
  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.mi_ig.id
  }
}

# 4. SUBRED PÚBLICA
resource "oci_core_subnet" "mi_subnet" {
  cidr_block        = "10.0.1.0/24"
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.mi_red.id
  display_name      = "Subred-Publica"
  route_table_id    = oci_core_route_table.mi_rt.id
}

# 5. BUSCAR IMAGEN DE LINUX
data "oci_core_images" "oracle_linux" {
  compartment_id   = var.compartment_ocid
  operating_system = "Oracle Linux"
  operating_system_version = "8"
  shape            = "VM.Standard.A1.Flex" # Ojo: Cambia a VM.Standard.A1.Flex si usas esa capa gratuita
  sort_by          = "TIMECREATED"
  sort_order       = "DESC"
}

# 6. BUSCAR ZONA DE DISPONIBILIDAD
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_ocid
}

# 7. EL SERVIDOR
resource "oci_core_instance" "mi_servidor" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_ocid
  display_name        = "Servidor-SimpleRAG"
  shape               = "VM.Standard.A1.Flex" 

  create_vnic_details {
    subnet_id        = oci_core_subnet.mi_subnet.id
    assign_public_ip = true
  }

  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.oracle_linux.images[0].id
  }

  # Script de inicio para descargar tu app
  metadata = {
    ssh_authorized_keys = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDkfEJNjuUaJHQVVsb5tHsN3tJyMPb4YCeC05LyiWmOp6fChjCk0/MgT/5uLAFcGFjkPlsolwH3sr7SiRTy7VbF+jD8O/t0V3uK8wngvtLzEIkFopCjLLi4ec/J0B8BYqlV6qwez+wwnZAJUXCXC2dI+txYC0QBcoCQulc51mPVNbWCBe5Ns2S40QwgridrxnwGj/gjdRagjD2GI6e792+4q+g+oQ0ckI3RwSxM8AJN47o51ysO+2yk013y5sl1IXcLNBGswuxcIAt6MBrQr5FllIy/Y+w3O3JRulsBJGbYeK0Jp7z35XSQmg9DfJupabCgVINQjZuhkFzz5UKXMZ8VMmQyu4Qe1TrF1kUmGPVd5jH6J/c8Rd15XYhfulu8wriccbD7lPvtx64HIxyFUSgB8fRlpi2P1pAeURb6pKNQN6svle+WcBTBClK/osPoCTkBwEDxAbdRtgKlv9p4NQodHWR560gLqEnLHq667ayqPdEsGDaP2BE8er6E8Pub5BnksmL9FU7MnhuTQ1DSHmdUeqKT4un056wBybsb0ArP1HZzTBR5CmC/C8ni+PW83mFZiNKhuxnrBMeMpK55b5hKmJaYKyuIXfWBaEjfCiwuM6983JqZN2Slczj2B65XcMxpaMV/egvZFEnzmGB3YuRf9w59Bk8kfZYL1AXwh87n7w== oscarestud@aa5f2d900ce2"
    user_data = base64encode(<<-EOF
      #!/bin/bash
      sudo yum update -y
      sudo yum install -y git
      mkdir -p /home/opc/app
      git clone https://github.com/OBerme/SimpleRAG.git /home/opc/app/SimpleRAG
    EOF
    )
  }
}