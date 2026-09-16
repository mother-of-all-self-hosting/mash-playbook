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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Copyparty

The playbook can install and configure [Copyparty](https://copyparty.eu/) for you.

Copyparty is a portable file server with many features.

See the project's [documentation](https://github.com/9001/copyparty/blob/hovudstraum/README.md) to learn what Copyparty does and why it might be useful to you.

For details about configuring the [Ansible role for Copyparty](https://radicle.network/nodes/iris.radicle.network/rad%3Az4GaYR5FxcSuYuCKovEo9Zfm3HPXc), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az4GaYR5FxcSuYuCKovEo9Zfm3HPXc/tree/docs/configuring-copyparty.md) online
- 📁 `roles/galaxy/copyparty/docs/configuring-copyparty.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# copyparty                                                            #
#                                                                      #
########################################################################

copyparty_enabled: true

copyparty_hostname: copyparty.example.com

########################################################################
#                                                                      #
# /copyparty                                                           #
#                                                                      #
########################################################################
```

### Set administrator password

By default it is necessary to create an administrator account, whose default username is set to `copyparty`. See [this section](https://radicle.network/nodes/iris.radicle.network/rad:z4GaYR5FxcSuYuCKovEo9Zfm3HPXc/tree/docs/configuring-copyparty.md#set-username-and-password) on the role's documentation for details.

## Usage

After running the command for installation, the Copyparty instance becomes available at the URL specified with `copyparty_hostname`. With the configuration above, the service is hosted at `https://copyparty.example.com`.

By default uploading is limited to the administrator account only. If you want to allow others (with or without accounts) upload, move, or delete files, it is necessary to specify corresponding permissions by recreating the default settings specified to `copyparty_config_options_additional_configuration`.

Refer to [this page](https://copyparty.eu/cli/) for the exhaustive list of available options.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az4GaYR5FxcSuYuCKovEo9Zfm3HPXc/tree/docs/configuring-copyparty.md#troubleshooting) on the role's documentation for details.
