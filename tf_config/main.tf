

# -----------------------------------------------------------------------
# 2. RED (VCN) - La carretera principal
# -----------------------------------------------------------------------
resource "oci_core_vcn" "mi_red" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = var.compartment_ocid
  display_name   = "Red-SimpleRAG"
}

# Puerta de enlace para tener Internet
resource "oci_core_internet_gateway" "mi_ig" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.mi_red.id
  display_name   = "InternetGateway"
}

# Mapa de carreteras (Tabla de rutas)
resource "oci_core_route_table" "mi_rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.mi_red.id
  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.mi_ig.id
  }
}

# -----------------------------------------------------------------------
# 3. FIREWALL (SECURITY LIST) - Aquí abrimos los puertos de tu App
# -----------------------------------------------------------------------
resource "oci_core_security_list" "mi_firewall_app" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.mi_red.id
  display_name   = "Reglas-App-RAG"

  # REGLA 1: SSH (Puerto 22) - Para que tú puedas entrar
  ingress_security_rules {
    protocol = "6" # TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 22
      max = 22
    }
  }

  # REGLA 2: STREAMLIT (Puerto 8501) - Tu página web
  ingress_security_rules {
    protocol = "6" # TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 8501
      max = 8501
    }
  }

  
  # NOTA: El puerto 8001 (Base de datos) NO se abre al público por seguridad.
  # Los contenedores se comunicarán internamente.

}

# -----------------------------------------------------------------------
# 4. SUBRED PÚBLICA - Donde vive el servidor
# -----------------------------------------------------------------------
resource "oci_core_subnet" "mi_subnet" {
  cidr_block        = "10.0.1.0/24"
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.mi_red.id
  display_name      = "Subred-Publica"
  route_table_id    = oci_core_route_table.mi_rt.id
  # AQUÍ VINCULAMOS EL FIREWALL QUE CREAMOS ARRIBA
  security_list_ids = [oci_core_security_list.mi_firewall_app.id]
}

# Buscamos la imagen de Ubuntu 22.04 que sea compatible con tu forma ARM
data "oci_core_images" "ubuntu_amd" {
  compartment_id           = var.compartment_ocid # O tu OCID directo si no usas vars
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "22.04"
  shape                    = "VM.Standard.E2.1.Micro" # <--- ESTA ES LA CLAVE
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_ocid
}

# -----------------------------------------------------------------------
# 6. EL SERVIDOR (INSTANCIA) - La máquina final
# -----------------------------------------------------------------------
resource "oci_core_instance" "mi_servidor" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_ocid
  display_name        = "Servidor-SimpleRAG-AMD"  
  shape               = "VM.Standard.E2.1.Micro"

  create_vnic_details {
    subnet_id        = oci_core_subnet.mi_subnet.id
    assign_public_ip = true
  }

  source_details {
    source_type = "image"
    # Aquí le decimos que coja el ID que ha encontrado el bloque 'data' de arriba
    source_id   = data.oci_core_images.ubuntu_amd.images[0].id 
  }

  # -----------------------------------------------------------
  # AQUÍ ESTÁ LA MAGIA: CONFIGURACIÓN AUTOMÁTICA
  # -----------------------------------------------------------
  metadata = {
    # 1. CAMBIO OBLIGATORIO: PEGA TU CLAVE PÚBLICA AQUÍ (la que empieza por ssh-rsa...)
    ssh_authorized_keys = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDkfEJNjuUaJHQVVsb5tHsN3tJyMPb4YCeC05LyiWmOp6fChjCk0/MgT/5uLAFcGFjkPlsolwH3sr7SiRTy7VbF+jD8O/t0V3uK8wngvtLzEIkFopCjLLi4ec/J0B8BYqlV6qwez+wwnZAJUXCXC2dI+txYC0QBcoCQulc51mPVNbWCBe5Ns2S40QwgridrxnwGj/gjdRagjD2GI6e792+4q+g+oQ0ckI3RwSxM8AJN47o51ysO+2yk013y5sl1IXcLNBGswuxcIAt6MBrQr5FllIy/Y+w3O3JRulsBJGbYeK0Jp7z35XSQmg9DfJupabCgVINQjZuhkFzz5UKXMZ8VMmQyu4Qe1TrF1kUmGPVd5jH6J/c8Rd15XYhfulu8wriccbD7lPvtx64HIxyFUSgB8fRlpi2P1pAeURb6pKNQN6svle+WcBTBClK/osPoCTkBwEDxAbdRtgKlv9p4NQodHWR560gLqEnLHq667ayqPdEsGDaP2BE8er6E8Pub5BnksmL9FU7MnhuTQ1DSHmdUeqKT4un056wBybsb0ArP1HZzTBR5CmC/C8ni+PW83mFZiNKhuxnrBMeMpK55b5hKmJaYKyuIXfWBaEjfCiwuM6983JqZN2Slczj2B65XcMxpaMV/egvZFEnzmGB3YuRf9w59Bk8kfZYL1AXwh87n7w== oscarestud@aa5f2d900ce2"
    
    # 2. SCRIPT DE INSTALACIÓN
    user_data = base64encode(<<-EOF
      #!/bin/bash
      apt-get update -y
      apt-get install -y git curl
      
      # 2. Instalar Docker y el plugin de Docker Compose desde los repos de Ubuntu
      # (Es más fiable que añadir repos externos en un script desatendido)
      apt-get install -y docker.io docker-compose-v2
      
      # 3. Arrancar Docker y configurarlo para que inicie siempre
      systemctl enable --now docker
      
      # 4. Añadir el usuario 'ubuntu' al grupo docker para no necesitar sudo
      usermod -aG docker ubuntu
      
      # 5. Preparar carpetas (Usamos /home/ubuntu, NO /home/opc)
      mkdir -p /home/ubuntu/app
      
      # 6. Clonar tu repositorio
      # Si el repo es público funcionará directo. Si es privado, necesitarás tokens.
      git clone https://github.com/OBerme/SimpleRAG.git /home/ubuntu/app/SimpleRAG
      
      # 7. Asegurar permisos correctos (para que el usuario ubuntu sea el dueño)
      chown -R ubuntu:ubuntu /home/ubuntu/app
      
      # 8. Desplegar
      cd /home/ubuntu/app/SimpleRAG
      
      # Ejecutamos docker compose
      # Nota: usamos la ruta completa del plugin por seguridad o el comando nuevo
      docker compose up -d --build
    EOF
    )
  }
}