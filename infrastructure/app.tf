variable "www_replicas" {
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

variable "discord_guild_id" {
  type = string
}

variable "discord_welcome_channel_id" {
  type = string
}

variable "discord_moderator_role_id" {
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

locals {
  app_config = {
    "TLS_CERTIFICATE"             = "${acme_certificate.www_certificate.certificate_pem}${acme_certificate.www_certificate.issuer_pem}"
    "TLS_PRIVATE_KEY"             = acme_certificate.www_certificate.private_key_pem
    "SECRET_KEY"                  = random_string.django_secret.result
    "APP_HOST"                    = var.app_hostname
    "DB_HOST"                     = digitalocean_database_cluster.postgres.private_host
    "DB_PORT"                     = digitalocean_database_cluster.postgres.port
    "DB_USER"                     = digitalocean_database_user.db.name
    "DB_PASSWORD"                 = digitalocean_database_user.db.password
    "DB_NAME"                     = digitalocean_database_db.db.name
    "DB_SSL_MODE"                 = "require"
    "REDIS_URI"                   = "rediss://${digitalocean_database_cluster.queue.user}:${digitalocean_database_cluster.queue.password}@${digitalocean_database_cluster.queue.private_host}:${digitalocean_database_cluster.queue.port}"
    "DISCORD_OAUTH_CLIENT_ID"     = var.discord_oauth_client_id
    "DISCORD_OAUTH_CLIENT_SECRET" = var.discord_oauth_client_secret
    "DISCORD_OAUTH_BOT_TOKEN"     = var.discord_oauth_bot_token
    "DISCORD_GUILD_ID"            = var.discord_guild_id
    "DISCORD_MODERATOR_ROLE_ID"   = var.discord_moderator_role_id
    "DISCORD_WELCOME_CHANNEL_ID"  = var.discord_welcome_channel_id
  }
}

resource "kubernetes_deployment" "virtualbarcamp_www" {
  metadata {
    name = "virtualbarcamp-www"

    annotations = {}
    labels      = {}
  }

  spec {
    replicas = var.workers

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

          dynamic "env" {
            for_each = local.app_config

            content {
              name  = env.key
              value = env.value
            }
          }
        }

        node_selector = {}
      }
    }
  }

  wait_for_rollout = false

  lifecycle {
    ignore_changes = [
      spec[0].template[0].spec[0].active_deadline_seconds,
      spec[0].template[0].spec[0].automount_service_account_token,
      spec[0].template[0].spec[0].container[0].command,
    ]
  }
}

resource "kubernetes_deployment" "virtualbarcamp_worker" {
  metadata {
    name = "virtualbarcamp-worker"

    annotations = {}
    labels      = {}
  }

  spec {
    replicas = 1

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

          dynamic "env" {
            for_each = local.app_config

            content {
              name  = env.key
              value = env.value
            }
          }
        }

        node_selector = {}
      }
    }
  }

  wait_for_rollout = false

  lifecycle {
    ignore_changes = [
      spec[0].template[0].spec[0].active_deadline_seconds,
      spec[0].template[0].spec[0].automount_service_account_token,
      spec[0].template[0].spec[0].container[0].command,
    ]
  }
}

resource "kubernetes_deployment" "virtualbarcamp_beat" {
  metadata {
    name = "virtualbarcamp-beat"

    annotations = {}
    labels      = {}
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
          args  = ["beat"]

          dynamic "env" {
            for_each = local.app_config

            content {
              name  = env.key
              value = env.value
            }
          }
        }

        node_selector = {}
      }
    }
  }

  wait_for_rollout = false

  lifecycle {
    ignore_changes = [
      spec[0].template[0].spec[0].active_deadline_seconds,
      spec[0].template[0].spec[0].automount_service_account_token,
      spec[0].template[0].spec[0].container[0].command,
    ]
  }
}

resource "kubernetes_deployment" "virtualbarcamp_bot" {
  metadata {
    name = "virtualbarcamp-bot"

    annotations = {}
    labels      = {}
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "virtualbarcamp-bot"
      }
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name" = "virtualbarcamp-bot"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.gitlab_registry_token.metadata[0].name
        }

        container {
          name  = "www"
          image = "registry.gitlab.com/cnorthwood/virtualbarcamp:${var.app_version}"
          args  = ["bot"]

          dynamic "env" {
            for_each = local.app_config

            content {
              name  = env.key
              value = env.value
            }
          }
        }

        node_selector = {}
      }
    }
  }

  wait_for_rollout = false

  lifecycle {
    ignore_changes = [
      spec[0].template[0].spec[0].active_deadline_seconds,
      spec[0].template[0].spec[0].automount_service_account_token,
      spec[0].template[0].spec[0].container[0].command,
    ]
  }
}
