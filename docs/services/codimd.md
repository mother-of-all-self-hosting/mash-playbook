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

# CodiMD

The playbook can install and configure [CodiMD](https://github.com/hackmdio/codimd) for you.

CodiMD is a realtime collaborative markdown notes on all platforms.

See the project's [documentation](https://hackmd.io/c/codimd-documentation) to learn what CodiMD does and why it might be useful to you.

For details about configuring the [Ansible role for CodiMD](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azp12kTQqmgqnFpUU6gPyVq19HNMD), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azp12kTQqmgqnFpUU6gPyVq19HNMD/tree/docs/configuring-codimd.md) online
- 📁 `roles/galaxy/codimd/docs/configuring-codimd.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md)
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# codimd                                                               #
#                                                                      #
########################################################################

codimd_enabled: true

codimd_hostname: codimd.example.com

########################################################################
#                                                                      #
# /codimd                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting CodiMD under a subpath (by configuring the `codimd_path_prefix` variable) does not seem to be possible due to CodiMD's technical limitations.

### Select database to use

It is necessary to select a database used by CodiMD from a MySQL compatible database and Postgres. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azp12kTQqmgqnFpUU6gPyVq19HNMD/tree/docs/configuring-codimd.md#specify-database) on the role's documentation for details.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
# Control if email sign-in is allowed
codimd_environment_variables_cmd_email: true

# Control if email registration is allowed
codimd_environment_variables_cmd_allow_email_register: true
```

See [this section](https://hackmd.io/c/codimd-documentation/%2Fs%2Fcodimd-configuration#Authentication) on the official documentation for details about setting up other authentication system like LDAP and OAuth.

## Usage

After running the command for installation, the CodiMD instance becomes available at the URL specified with `codimd_hostname`. With the configuration above, the service is hosted at `https://codimd.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azp12kTQqmgqnFpUU6gPyVq19HNMD/tree/docs/configuring-codimd.md#troubleshooting) on the role's documentation for details.
