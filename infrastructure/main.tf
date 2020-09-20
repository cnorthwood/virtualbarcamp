variable "do_token" {
  type = string
}

provider "digitalocean" {
  token = var.do_token
}

variable "workers" {
  type    = number
  default = 1
}

variable "node_size" {
  type    = string
  default = "s-1vcpu-2gb"
}

variable "do_region" {
  type    = string
  default = "lon1"
}

data "digitalocean_kubernetes_versions" "versions" {}

provider "kubernetes" {
  load_config_file = false
  host             = digitalocean_kubernetes_cluster.virtualbarcamp.endpoint
  token            = digitalocean_kubernetes_cluster.virtualbarcamp.kube_config[0].token
  cluster_ca_certificate = base64decode(
    digitalocean_kubernetes_cluster.virtualbarcamp.kube_config[0].cluster_ca_certificate
  )
}

resource "digitalocean_vpc" "vpc" {
  name   = "virtualbarcamp"
  region = var.do_region
}

resource "digitalocean_kubernetes_cluster" "virtualbarcamp" {
  name         = "virtualbarcamp"
  region       = var.do_region
  version      = data.digitalocean_kubernetes_versions.versions.latest_version
  auto_upgrade = true
  vpc_uuid     = digitalocean_vpc.vpc.id

  node_pool {
    name       = "virtualbarcamp"
    size       = var.node_size
    node_count = var.workers
  }
}
