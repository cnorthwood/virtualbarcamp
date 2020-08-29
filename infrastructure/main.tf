variable "do_token" {
  type = string
}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_kubernetes_versions" "versions" {}

provider "kubernetes" {
  load_config_file = false
  host             = digitalocean_kubernetes_cluster.barcampmanchester.endpoint
  token            = digitalocean_kubernetes_cluster.barcampmanchester.kube_config[0].token
  cluster_ca_certificate = base64decode(
    digitalocean_kubernetes_cluster.barcampmanchester.kube_config[0].cluster_ca_certificate
  )
}

resource "digitalocean_vpc" "vpc" {
  name   = "barcampmanchester"
  region = "lon1"
}

resource "digitalocean_kubernetes_cluster" "barcampmanchester" {
  name         = "barcampmanchester"
  region       = "lon1"
  version      = data.digitalocean_kubernetes_versions.versions.latest_version
  auto_upgrade = true
  vpc_uuid     = digitalocean_vpc.vpc.id

  node_pool {
    name       = "barcampmanchester"
    size       = "s-1vcpu-2gb"
    node_count = 1
  }
}
