<!--
SPDX-FileCopyrightText: 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Headscale

The playbook can install and configure [Headscale](https://headscale.net/) for you.

Headscale is an open-source, self-hosted implementation of the [Tailscale](https://tailscale.com/) control server.

See the project's [documentation](https://headscale.net/stable/usage/getting-started/) to learn what Headscale does and why it might be useful to you.

For details about configuring the [Ansible role for Headscale](https://github.com/mother-of-all-self-hosting/ansible-role-headscale), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-headscale/blob/main/docs/configuring-headscale.md) online
- 📁 `roles/galaxy/headscale/docs/configuring-headscale.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# headscale                                                            #
#                                                                      #
########################################################################

headscale_enabled: true

headscale_hostname: headscale.example.com

########################################################################
#                                                                      #
# /headscale                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Headscale instance becomes available at the URL specified with `headscale_hostname` and `headscale_path_prefix`. With the configuration above, the service is hosted at `https://headscale.example.com`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-headscale/blob/main/docs/configuring-headscale.md#usage) on the role's documentation for details about how to use Headscale.

## Related services

- [Headplane](headplane.md) — Feature-complete [Tailscale Web UI](https://tailscale.com/) for Headscale
