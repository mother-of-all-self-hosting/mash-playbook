<!--
SPDX-FileCopyrightText: 2025 spatterlight
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Headplane

The playbook can install and configure [Headplane](https://headplane.net/) for you.

Headplane is an open-source, self-hosted implementation of the [Tailscale Web UI](https://tailscale.com/) for [Headscale](headscale.md).

See the project's [documentation](https://headplane.net/introduction) to learn what Headplane does and why it might be useful to you.

For details about configuring the [Ansible role for Headplane](https://github.com/spatterIight/ansible-role-headplane), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-headplane/blob/main/docs/configuring-headplane.md) online
- 📁 `roles/galaxy/headplane/docs/configuring-headplane.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Headscale](headscale.md) server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# headplane                                                            #
#                                                                      #
########################################################################

headplane_enabled: true

headplane_hostname: headplane.example.com

########################################################################
#                                                                      #
# /headplane                                                           #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/spatterIight/ansible-role-headplane/blob/main/docs/configuring-headplane.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings.

## Usage

After running the command for installation, the Headplane instance becomes available at the URL specified with `headplane_hostname`. With the configuration above, the service is hosted at `https://headplane.example.com/admin`.

Refer to [this section](https://github.com/spatterIight/ansible-role-headplane/blob/main/docs/configuring-headplane.md#usage) on the role's documentation for details about the usage.
