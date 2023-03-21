# Supported services

|              Name              |              Description              | Documentation |
| ------------------------------ | ------------------------------------- | ------------- |
| [Collabora Online](https://www.collaboraoffice.com/) | Your Private Office Suite In The Cloud | [Link](services/collabora-online.md) |
| [Docker](https://www.docker.com/) | Open-source software for deploying containerized applications | [Link](services/docker.md) |
| [Docker Registry](https://docs.docker.com/registry/) | A container image distribution registry | [Link](services/docker-registry.md) |
| [Docker Registry Browser](https://github.com/klausmeyer/docker-registry-browser) | Web Interface for the Docker Registry HTTP API V2 written in Ruby on Rails | [Link](services/docker-registry-browser.md) |
| [Docker Registry Purger](https://github.com/devture/docker-registry-purger) | A small tool used for purging a private Docker Registry's old tags | [Link](services/docker-registry-purger.md) |
| [Focalboard](https://www.focalboard.com/) | An open source, self-hosted alternative to [Trello](https://trello.com/), [Notion](https://www.notion.so/), and [Asana](https://asana.com/). | [Link](services/focalboard.md) |
| [Gitea](https://gitea.io/) | A painless self-hosted Git service. | [Link](services/gitea.md) |
| [Grafana](https://grafana.com/) | An open and composable observability and data visualization platform, often used with [Prometheus](services/prometheus.md) | [Link](services/grafana.md) | 
| [Hubsite](https://github.com/moan0s/hubsite) | A simple, static site that shows an overview of the available services | [Link](services/hubsite.md) | 
| [Miniflux](https://miniflux.app/) | Minimalist and opinionated feed reader. | [Link](services/miniflux.md) |
| [Nextcloud](https://nextcloud.com/) | The most popular self-hosted collaboration solution for tens of millions of users at thousands of organizations across the globe. | [Link](services/nextcloud.md) |
| [PeerTube](https://joinpeertube.org/) | A tool for sharing online videos | [Link](services/peertube.md) |
| [Postgres](https://www.postgresql.org) | A powerful, open source object-relational database system | [Link](services/postgres.md) |
| [Postgres Backup](https://github.com/prodrigestivill/docker-postgres-backup-local) | A solution for backing up PostgresSQL to local filesystem with periodic backups. | [Link](services/postgres-backup.md) |
| [Prometheus](https://prometheus.io/) | A metrics collection and alerting monitoring solution | [Link](services/prometheus.md) |
| [Prometheus Node Exporter](https://github.com/prometheus/node_exporter) | Exporter for machine metrics | [Link](services/prometheus-node-exporter.md) |
| [Prometheus Blackbox Exporter](https://github.com/prometheus/blackbox_exporter) | Blackbox probing of HTTP/HTTPS/DNS/TCP/ICMP and gRPC endpoints | [Link](services/prometheus-blackbox-exporter.md) |
| [Radicale](https://radicale.org/) | A Free and Open-Source CalDAV and CardDAV Server (solution for hosting contacts and calendars) | [Link](services/radicale.md) |
| [Redmine](https://redmine.org/) | A flexible project management web application. | [Link](services/redmine.md) |
| [Redis](https://redis.io/) | An in-memory data store used by millions of developers as a database, cache, streaming engine, and message broker. | [Link](services/redis.md) |
| [Traefik](https://doc.traefik.io/traefik/) | A container-aware reverse-proxy server | [Link](services/traefik.md) |
| [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | A lightweight unofficial and compatible implementation of the [Bitwarden](https://bitwarden.com/) password manager | [Link](services/vaultwarden.md) |
| [Uptime-kuma](https://uptime.kuma.pet/) | A fancy self-hosted monitoring tool | [Link](services/uptime-kuma.md) |
| [Woodpecker CI](https://woodpecker-ci.org/) | A simple Continuous Integration (CI) engine with great extensibility. | [Link](services/woodpecker-ci.md) |
| System-related | A collection of various system-related components | [Link](services/system.md) |


## Related playbooks

- [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) - for deploying a fully-featured [Matrix](https://matrix.org) homeserver. This playbook will remain independent, because the Matrix ecosystem is incredibly large - lots of bots, bridges and other pieces of software. It deserves its own dedicated playbook.


## Coming soon

|              Name              |              Description              |
| ------------------------------ | ------------------------------------- |
| [Garage](https://garagehq.deuxfleurs.fr/), by absorbing [garage-docker-ansible-deploy](https://github.com/moan0s/garage-docker-ansible-deploy) | Open-source distributed object storage service tailored for self-hosting |

