## Copyright (c) 2022, Oracle and/or its affiliates. 
## All rights reserved. The Universal Permissive License (UPL), Version 1.0 as shown at http://oss.oracle.com/licenses/upl

terraform {
  required_version = ">= 0.14"
  required_providers {
    oci = {
      source = "hashicorp/oci"
      # version = "4.34.0"
    }
    tls = {
      source  = "hashicorp/tls"
    
    }
    local = {
      source  = "hashicorp/local"

    }
    random = {
      source  = "hashicorp/random"
    
    }
  }
}

provider "oci" {
  region       = var.region
}

provider "oci" {
  alias        = "home_region"
  tenancy_ocid = var.tenancy_ocid
  region       = lookup(data.oci_identity_regions.home_region.regions[0], "name")
}

provider "oci" {
  alias        = "current_region"
  tenancy_ocid = var.tenancy_ocid
  region       = var.region
}
