provider "acme" {
  server_url = "https://acme-v02.api.letsencrypt.org/directory"
}

resource "digitalocean_domain" "online_barcampmanchester_co_uk" {
  name       = "online.barcampmanchester.co.uk"
  ip_address = "159.65.215.5"
}

resource "tls_private_key" "online_barcampmanchester_co_uk" {
  algorithm = "RSA"
}

resource "acme_registration" "registration" {
  account_key_pem = tls_private_key.online_barcampmanchester_co_uk.private_key_pem
  email_address   = "chris@barcampmanchester.co.uk"
}

resource "acme_certificate" "online_barcampmanchester_co_uk" {
  account_key_pem = acme_registration.registration.account_key_pem
  common_name     = "online.barcampmanchester.co.uk"

  dns_challenge {
    provider = "digitalocean"
    config = {
      DO_AUTH_TOKEN = var.do_token
    }
  }
}

resource "kubernetes_service" "www" {
  metadata {
    name = "www"

    annotations = {
      "kubernetes.digitalocean.com/load-balancer-id"         = ""
      "service.beta.kubernetes.io/do-loadbalancer-algorithm" = "least_connections"
      "service.beta.kubernetes.io/do-loadbalancer-hostname"  = "online.barcampmanchester.co.uk"
    }
  }

  spec {
    type = "LoadBalancer"

    selector = {
      "app.kubernetes.io/name" = "virtualbarcamp"
    }

    port {
      port        = "80"
      target_port = "8080"
      name        = "http"
    }

    port {
      port        = "443"
      target_port = "8443"
      name        = "https"
    }
  }

  lifecycle {
    ignore_changes = [
      metadata[0].annotations["kubernetes.digitalocean.com/load-balancer-id"],
    ]
  }
}
