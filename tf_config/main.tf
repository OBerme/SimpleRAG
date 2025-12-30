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
    ssh_authorized_keys = "PEGA_AQUI_TU_CLAVE_PUBLICA_SSH_SI_QUIERES_ENTRAR"
    user_data = base64encode(<<-EOF
      #!/bin/bash
      sudo yum update -y
      sudo yum install -y git
      mkdir -p /home/opc/app
      git clone https://github.com/tu-usuario/SimpleRAG.git /home/opc/app/SimpleRAG
    EOF
    )
  }
}