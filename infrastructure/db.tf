resource "digitalocean_database_cluster" "postgres" {
  name                 = "virtualbarcampdb"
  engine               = "pg"
  version              = "12"
  size                 = "db-s-1vcpu-1gb"
  region               = "lon1"
  node_count           = 1
  private_network_uuid = digitalocean_vpc.vpc.id
}

resource "digitalocean_database_firewall" "db_firewall" {
  cluster_id = digitalocean_database_cluster.postgres.id
  rule {
    type  = "k8s"
    value = digitalocean_kubernetes_cluster.virtualbarcamp.id
  }
}

resource "digitalocean_database_db" "db" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "virtualbarcamp"
}

resource "digitalocean_database_user" "db" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "virtualbarcamp"
}
