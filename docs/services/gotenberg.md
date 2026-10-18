<!--
SPDX-FileCopyrightText: 2021 foxcris
SPDX-FileCopyrightText: 2021-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Gotenberg

The playbook can install and configure [Gotenberg](https://gotenberg.dev/) for you.

Gotenberg is a Docker-based API for converting documents to PDF.

For details about configuring the [Ansible role for Gotenberg](https://github.com/mother-of-all-self-hosting/ansible-role-gotenberg), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gotenberg/blob/main/docs/configuring-gotenberg.md) online
- 📁 `roles/galaxy/gotenberg/docs/configuring-gotenberg.md` locally, if you have [fetched the Ansible roles](../installing.md)

### Integrating with Prometheus (optional)

Gotenberg can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Gotenberg and Prometheus do not share a network (like Traefik), you can connect the Gotenberg container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ gotenberg_container_network }}"
```

#### Expose metrics publicly

If Gotenberg metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-gotenberg`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
gotenberg_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
gotenberg_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Related services

- [Apache Tika Server](tika.md) — Detect and extract metadata and text from different file types (such as PPT, XLS, and PDF)
- [Paperless-ngx](paperless-ngx.md) — Document management system that transforms your physical documents into a searchable online archive
