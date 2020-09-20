resource "digitalocean_database_cluster" "queue" {
  name                 = "virtualbarcampqueue"
  engine               = "redis"
  version              = "5"
  size                 = "db-s-1vcpu-1gb"
  region               = digitalocean_vpc.vpc.region
  node_count           = 1
  private_network_uuid = digitalocean_vpc.vpc.id
}

resource "digitalocean_database_firewall" "queue_firewall" {
  cluster_id = digitalocean_database_cluster.queue.id
  rule {
    type  = "k8s"
    value = digitalocean_kubernetes_cluster.virtualbarcamp.id
  }
}
