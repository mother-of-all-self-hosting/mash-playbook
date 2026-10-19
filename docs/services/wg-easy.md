<!--
SPDX-FileCopyrightText: 2023-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# WireGuard Easy

The playbook can install and configure [WireGuard Easy](https://github.com/wg-easy/wg-easy) for you.

WireGuard Easy is the easiest way to run [WireGuard](https://www.wireguard.com/) VPN + Web-based Admin UI.

See the project's [documentation](https://wg-easy.github.io/wg-easy/latest/) to learn what WireGuard Easy does and why it might be useful to you.

For details about configuring the [Ansible role for WireGuard Easy](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy/blob/main/docs/configuring-wg-easy.md) online
- 📁 `roles/galaxy/wg_easy/docs/configuring-wg-easy.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- Modern Linux kernel which supports WireGuard
- `devture_systemd_docker_base_ipv6_enabled: true` if you'd like IPv6 support

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# wg-easy                                                              #
#                                                                      #
########################################################################

wg_easy_enabled: true

wg_easy_hostname: wg-easy.example.com

########################################################################
#                                                                      #
# /wg-easy                                                             #
#                                                                      #
########################################################################
```

>[!NOTE]
> There are a few variables that you may wish to adjust before doing the initial [unattended setup](https://github.com/wg-easy/wg-easy/blob/v15.2.0/docs/content/advanced/config/unattended-setup.md). The reason it's important to do this early on is because certain variables (`wg_easy_environment_variables_additional_variable_init_*`) **only take effect during the initial setup phase**.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy/blob/main/docs/configuring-wg-easy.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings such as [setting details for the initial setup user](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy/blob/main/docs/configuring-wg-easy.md#setting-details-for-the-initial-setup-user-optional), [adjusting the Wireguard endpoint](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy/blob/main/docs/configuring-wg-easy.md#adjusting-the-wireguard-endpoint), etc.

### Integrating with Prometheus (optional)

WireGuard Easy can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If WireGuard Easy and Prometheus do not share a network (like Traefik), you can connect the WireGuard Easy container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ wg_easy_container_network }}"
```

#### Expose metrics publicly

If WireGuard Easy metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-wg-easy`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
wg_easy_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
wg_easy_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the WireGuard Easy instance becomes available at the URL specified with `wg_easy_hostname`. With the configuration above, the service is hosted at `wg-easy.example.com`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy/blob/main/docs/configuring-wg-easy.md#usage) on the role's documentation for details about the usage such as [creating WireGuard clients](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy/blob/main/docs/configuring-wg-easy.md#creating-wireguard-clients) and [creating additional users](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy/blob/main/docs/configuring-wg-easy.md#creating-additional-users), etc.

## Related services

- [AdGuard Home](adguard-home.md) — A network-wide DNS software for blocking ads & tracking
