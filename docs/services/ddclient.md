<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ddclient

The playbook can install and configure [ddclient](https://docs.ddclient.io) for you.

ddclient allows to deploy headless browsers in Docker.

See the project's [documentation](https://docs.ddclient.io/enterprise/quick-start) to learn what ddclient does and why it might be useful to you.

For details about configuring the [Ansible role for ddclient](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md) online
- 📁 `roles/galaxy/ddclient/docs/configuring-ddclient.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — a reverse-proxy server for exposing ddclient publicly

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ddclient                                                             #
#                                                                      #
########################################################################

ddclient_enabled: true

########################################################################
#                                                                      #
# /ddclient                                                            #
#                                                                      #
########################################################################
```

### Expose the instance publicly (optional)

By default, the ddclient instance is not exposed externally, as it is mainly intended to be used in the internal network.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which ddclient is served.
ddclient_hostname: "ddclient.example.com"
```

**Note**: hosting ddclient under a subpath (by configuring the `ddclient_path_prefix` variable) does not seem to be possible due to ddclient's technical limitations.

## Usage

After running the command for installation, ddclient becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the URL specified with `ddclient_hostname`. With the configuration above, the service is hosted at `https://ddclient.example.com`.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md#troubleshooting) on the role's documentation for details.
