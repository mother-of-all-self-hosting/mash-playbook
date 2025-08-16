<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 - 2025 MASH project contributors
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# linkding

The playbook can install and configure [linkding](https://linkding.link) for you.

linkding is a bookmark manager that is designed be to be minimal and fast.

See the project's [documentation](https://linkding.link/installation/) to learn what linkding does and why it might be useful to you.

For details about configuring the [Ansible role for linkding](https://github.com/mother-of-all-self-hosting/ansible-role-linkding), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-linkding/blob/main/docs/configuring-linkding.md) online
- 📁 `roles/galaxy/linkding/docs/configuring-linkding.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) a [Postgres](postgres.md) database — linkding will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# linkding                                                             #
#                                                                      #
########################################################################

linkding_enabled: true

linkding_hostname: mash.example.com
linkding_path_prefix: /linkding

linkding_superuser_username: ''
linkding_superuser_password: ''

########################################################################
#                                                                      #
# /linkding                                                            #
#                                                                      #
########################################################################
```

### Configure superuser (optional)

You can optionally create an initial "superuser". See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-linkding/blob/main/docs/configuring-linkding.md#configure-superuser-optional) on the role's documentation for details.

## Usage

After running the command for installation, the linkding instance becomes available at the URL specified with `linkding_hostname` and `linkding_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/linkding`.

To get started, open the URL with a web browser, and log in with the superuser's login credential.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-linkding/blob/main/docs/configuring-linkding.md#troubleshooting) on the role's documentation for details.
