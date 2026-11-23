<!--
SPDX-FileCopyrightText: 2026 sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# CrowdSec

The playbook can install [CrowdSec](https://www.crowdsec.net/) for behavioral detection from logs and IP remediation.

When playbook-managed Traefik is enabled, this component automatically joins its private Docker network, acquires Traefik and SSH journal logs, and enables the Traefik bouncer middleware on the HTTPS entrypoint. This protects HTTP services behind that Traefik without per-service configuration. CrowdSec's Local API is not published on a host port.

Traefik access logs must remain enabled for HTTP detections; they are enabled by default by the playbook's Traefik role.

The CrowdSec Traefik parser supports both Traefik's default `common` access log format and JSON. This integration leaves the format unchanged; set `traefik_config_accessLog_format: json` if another log consumer requires it.

The bouncer uses CrowdSec's decision stream. `crowdsec_traefik_bouncer_stream_startup_block_enabled` defaults to `false` so a CrowdSec startup outage does not block every Traefik request; set it to `true` for fail-closed startup behavior.

For details about configuring the [Ansible role for CrowdSec](https://github.com/mother-of-all-self-hosting/ansible-role-crowdsec), see its [configuration guide](https://github.com/mother-of-all-self-hosting/ansible-role-crowdsec/blob/main/docs/configuring-crowdsec.md) or `roles/galaxy/crowdsec/docs/configuring-crowdsec.md` after [fetching the Ansible roles](../../docs/installing.md).

## Configuration

Enable CrowdSec in `vars.yml` and rerun the [installation](../../docs/installing.md):

```yaml
crowdsec_enabled: true
```

The role uses the Debian CrowdSec image to read journald without a Docker socket. It monitors SSH logs and, when managed Traefik is enabled, Traefik access logs. The corresponding Linux, SSH, and Traefik collections are installed automatically.

The Traefik bouncer applies to all routers on the managed HTTPS entrypoint. If Traefik is behind a CDN or another proxy, configure only its trusted IP ranges in Traefik; the bouncer uses the same list. Set `crowdsec_traefik_client_trusted_ips` for client addresses that should bypass remediation, such as a trusted LAN or VPN.

This does not block connections to ports exposed directly on the host. A firewall bouncer is intentionally not included in this first integration. If Traefik is externally managed, its plugin and middleware require manual configuration.

## Related services

- [Traefik](../traefik/README.md) — Reverse proxy automatically protected by the CrowdSec bouncer
