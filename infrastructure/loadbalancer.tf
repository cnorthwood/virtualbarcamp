provider "acme" {
  server_url = "https://acme-v02.api.letsencrypt.org/directory"
}

variable "app_hostname" {
  type = string
}

variable "letsencrypt_account_email" {
  type = string
}

resource "digitalocean_domain" "domain" {
  name       = var.app_hostname
  ip_address = data.digitalocean_loadbalancer.www.ip
}

resource "tls_private_key" "letsencrypt_account_key" {
  algorithm = "RSA"
}

resource "acme_registration" "registration" {
  account_key_pem = tls_private_key.letsencrypt_account_key.private_key_pem
  email_address   = var.letsencrypt_account_email
}

resource "acme_certificate" "www_certificate" {
  account_key_pem = acme_registration.registration.account_key_pem
  common_name     = var.app_hostname

  dns_challenge {
    provider = "digitalocean"
    config = {
      DO_AUTH_TOKEN = var.do_token
    }
  }

  depends_on = [digitalocean_domain.domain]
}

data "digitalocean_loadbalancer" "www" {
  name = kubernetes_service.www.metadata[0].annotations["service.beta.kubernetes.io/do-loadbalancer-name"]

  depends_on = [kubernetes_service.www]
}

resource "kubernetes_service" "www" {
  metadata {
    name = "www"

    annotations = {
      "kubernetes.digitalocean.com/load-balancer-id"         = ""
      "service.beta.kubernetes.io/do-loadbalancer-algorithm" = "least_connections"
      "service.beta.kubernetes.io/do-loadbalancer-hostname"  = var.app_hostname
      "service.beta.kubernetes.io/do-loadbalancer-name"      = "virtualbarcamp"
    }
  }

  spec {
    type = "LoadBalancer"

    selector = {
      "app.kubernetes.io/name" = "virtualbarcamp-www"
    }

    port {
      port        = "80"
      name        = "http"
      target_port = "8080"
    }

    port {
      port        = "443"
      name        = "https"
      target_port = "8443"
    }
  }

  lifecycle {
    ignore_changes = [
      metadata[0].annotations["kubernetes.digitalocean.com/load-balancer-id"],
    ]
  }
}
