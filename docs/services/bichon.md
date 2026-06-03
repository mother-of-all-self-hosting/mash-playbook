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

# Bichon

The playbook can install and configure [Bichon](https://github.com/rustmailer/bichon) for you.

Bichon is an email archiving server which downloads emails from IMAP accounts, builds a full-text search index, and serves a REST API with an embedded WebUI.

See the project's [documentation](https://github.com/rustmailer/bichon/blob/main/README.md) to learn what Bichon does and why it might be useful to you.

For details about configuring the [Ansible role for Bichon](https://radicle.network/nodes/iris.radicle.network/rad%3Az2nQcYvPh51zfvVu8hkftDYPmELYP), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az2nQcYvPh51zfvVu8hkftDYPmELYP/tree/docs/configuring-bichon.md) online
- 📁 `roles/galaxy/bichon/docs/configuring-bichon.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# bichon                                                               #
#                                                                      #
########################################################################

bichon_enabled: true

bichon_hostname: bichon.example.com

########################################################################
#                                                                      #
# /bichon                                                              #
#                                                                      #
########################################################################
```

### Set a random string

You also need to set a random secure string used for encrypting stored credentials. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
bichon_environment_variables_bichon_encrypt_password: YOUR_SECRET_KEY_HERE
```

## Usage

After running the command for installation, the Bichon instance becomes available at the URL specified with `bichon_hostname`. With the configuration above, the service is hosted at `https://bichon.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az2nQcYvPh51zfvVu8hkftDYPmELYP/tree/docs/configuring-bichon.md#troubleshooting) on the role's documentation for details.

## Related services

- [Open Archiver](openarchiver.md) — Archive, store, index, and search emails from various platforms, including generic IMAP-enabled email inboxes
