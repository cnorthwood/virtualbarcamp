variable "www_replicas" {
  type    = number
  default = 1
}

variable "worker_replicas" {
  type    = number
  default = 1
}

variable "app_version" {
  type = string
}

variable "gitlab_deploy_token_username" {
  type = string
}

variable "gitlab_deploy_token_password" {
  type = string
}

variable "discord_oauth_client_id" {
  type = string
}

variable "discord_oauth_client_secret" {
  type = string
}

variable "discord_oauth_bot_token" {
  type = string
}

provider "random" {}

resource "random_string" "django_secret" {
  length = 40
}

resource "kubernetes_secret" "gitlab_registry_token" {
  metadata {
    name = "gitlab-registry-token"
  }

  data = {
    ".dockerconfigjson" = jsonencode({
      auths = {
        "registry.gitlab.com" = {
          email = null
          auth : base64encode("${var.gitlab_deploy_token_username}:${var.gitlab_deploy_token_password}")
        }
      }
    })
  }

  type = "kubernetes.io/dockerconfigjson"
}

resource "kubernetes_service" "virtualbarcamp" {
  metadata {
    name = "virtualbarcamp"
  }

  spec {
    selector = {
      "app.kubernetes.io/name" = "virtualbarcamp-www"
    }
    port {
      name = "http"
      port = 8080
    }
    port {
      name = "https"
      port = 8443
    }
  }
}

resource "kubernetes_deployment" "virtualbarcamp_www" {
  metadata {
    name = "virtualbarcamp-www"
  }

  spec {
    replicas = var.www_replicas

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "virtualbarcamp-www"
      }
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name" = "virtualbarcamp-www"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.gitlab_registry_token.metadata[0].name
        }

        container {
          name  = "www"
          image = "registry.gitlab.com/cnorthwood/virtualbarcamp:${var.app_version}"
          args  = ["www"]

          env {
            name  = "TLS_CERTIFICATE"
            value = "${acme_certificate.online_barcampmanchester_co_uk.issuer_pem}\n${acme_certificate.online_barcampmanchester_co_uk.certificate_pem}"
          }

          env {
            name  = "TLS_PRIVATE_KEY"
            value = tls_private_key.online_barcampmanchester_co_uk.private_key_pem
          }

          env {
            name  = "SECRET_KEY"
            value = random_string.django_secret.result
          }

          env {
            name  = "DB_HOST"
            value = digitalocean_database_cluster.postgres.private_host
          }

          env {
            name  = "DB_PORT"
            value = digitalocean_database_cluster.postgres.port
          }

          env {
            name  = "DB_USER"
            value = digitalocean_database_user.db.name
          }

          env {
            name  = "DB_PASSWORD"
            value = digitalocean_database_user.db.password
          }

          env {
            name  = "DB_NAME"
            value = digitalocean_database_db.db.name
          }

          env {
            name  = "REDIS_HOST"
            value = digitalocean_database_cluster.queue.private_host
          }

          env {
            name  = "REDIS_PORT"
            value = digitalocean_database_cluster.queue.port
          }

          env {
            name  = "DISCORD_OAUTH_CLIENT_ID"
            value = var.discord_oauth_client_id
          }

          env {
            name  = "DISCORD_OAUTH_CLIENT_SECRET"
            value = var.discord_oauth_client_secret
          }

          env {
            name  = "DISCORD_OAUTH_BOT_TOKEN"
            value = var.discord_oauth_bot_token
          }
        }
      }
    }
  }
}

resource "kubernetes_deployment" "virtualbarcamp_worker" {
  metadata {
    name = "virtualbarcamp-worker"
  }

  spec {
    replicas = var.worker_replicas

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "virtualbarcamp-worker"
      }
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name" = "virtualbarcamp-worker"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.gitlab_registry_token.metadata[0].name
        }

        container {
          name  = "www"
          image = "registry.gitlab.com/cnorthwood/virtualbarcamp:${var.app_version}"
          args  = ["worker"]

          env {
            name  = "SECRET_KEY"
            value = random_string.django_secret.result
          }

          env {
            name  = "DB_HOST"
            value = digitalocean_database_cluster.postgres.private_host
          }

          env {
            name  = "DB_PORT"
            value = digitalocean_database_cluster.postgres.port
          }

          env {
            name  = "DB_USER"
            value = digitalocean_database_user.db.name
          }

          env {
            name  = "DB_PASSWORD"
            value = digitalocean_database_user.db.password
          }

          env {
            name  = "DB_NAME"
            value = digitalocean_database_db.db.name
          }

          env {
            name  = "REDIS_HOST"
            value = digitalocean_database_cluster.queue.private_host
          }

          env {
            name  = "REDIS_PORT"
            value = digitalocean_database_cluster.queue.port
          }

          env {
            name  = "DISCORD_OAUTH_CLIENT_ID"
            value = var.discord_oauth_client_id
          }

          env {
            name  = "DISCORD_OAUTH_CLIENT_SECRET"
            value = var.discord_oauth_client_secret
          }

          env {
            name  = "DISCORD_OAUTH_BOT_TOKEN"
            value = var.discord_oauth_bot_token
          }
        }
      }
    }
  }
}

resource "kubernetes_deployment" "virtualbarcamp_beat" {
  metadata {
    name = "virtualbarcamp-beat"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "virtualbarcamp-beat"
      }
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name" = "virtualbarcamp-beat"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.gitlab_registry_token.metadata[0].name
        }

        container {
          name  = "www"
          image = "registry.gitlab.com/cnorthwood/virtualbarcamp:${var.app_version}"
          args  = ["worker"]

          env {
            name  = "SECRET_KEY"
            value = random_string.django_secret.result
          }

          env {
            name  = "DB_HOST"
            value = digitalocean_database_cluster.postgres.private_host
          }

          env {
            name  = "DB_PORT"
            value = digitalocean_database_cluster.postgres.port
          }

          env {
            name  = "DB_USER"
            value = digitalocean_database_user.db.name
          }

          env {
            name  = "DB_PASSWORD"
            value = digitalocean_database_user.db.password
          }

          env {
            name  = "DB_NAME"
            value = digitalocean_database_db.db.name
          }

          env {
            name  = "REDIS_HOST"
            value = digitalocean_database_cluster.queue.private_host
          }

          env {
            name  = "REDIS_PORT"
            value = digitalocean_database_cluster.queue.port
          }

          env {
            name  = "DISCORD_OAUTH_CLIENT_ID"
            value = var.discord_oauth_client_id
          }

          env {
            name  = "DISCORD_OAUTH_CLIENT_SECRET"
            value = var.discord_oauth_client_secret
          }

          env {
            name  = "DISCORD_OAUTH_BOT_TOKEN"
            value = var.discord_oauth_bot_token
          }
        }
      }
    }
  }
}
