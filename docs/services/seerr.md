<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 sudo-Tiz
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Seerr

The playbook can install and configure [Seerr](https://github.com/seerr-team/seerr) for you.

Seerr is a media request and discovery manager with support for [Jellyfin](jellyfin.md), [Plex](plex.md), and Emby.

For details about configuring the [Ansible role for Seerr](https://github.com/spatterIight/ansible-role-seerr), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-seerr/blob/main/docs/configuring-seerr.md) online
- 📁 `roles/galaxy/seerr/docs/configuring-seerr.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# seerr                                                                #
#                                                                      #
########################################################################

seerr_enabled: true

seerr_hostname: seerr.example.com

########################################################################
#                                                                      #
# /seerr                                                               #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Seerr instance becomes available at the URL specified with `seerr_hostname`. With the configuration above, the service is hosted at `https://seerr.example.com`.

## Troubleshooting

Refer to [this section](https://github.com/spatterIight/ansible-role-seerr/blob/main/docs/configuring-seerr.md#troubleshooting) on the role's documentation for details.

## Related services

- [Jellyfin](jellyfin.md)
- [Plex](plex.md)
