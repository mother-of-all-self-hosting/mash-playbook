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
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Miniflux

The playbook can install and configure [Miniflux](https://miniflux.app/) for you.

Miniflux is a minimalist and opinionated feed reader.

See the project's [documentation](https://github.com/httpjamesm/Miniflux/blob/main/README.md) to learn what Miniflux does and why it might be useful to you.

For details about configuring the [Ansible role for Miniflux](https://github.com/mother-of-all-self-hosting/ansible-role-miniflux), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-miniflux/blob/main/docs/configuring-miniflux.md) online
- 📁 `roles/galaxy/miniflux/docs/configuring-miniflux.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# miniflux                                                             #
#                                                                      #
########################################################################

miniflux_enabled: true

miniflux_hostname: mash.example.com
miniflux_path_prefix: /miniflux

########################################################################
#                                                                      #
# /miniflux                                                            #
#                                                                      #
########################################################################
```

### Add configurations for admin user (optional)

If you wish to create an admin user on startup, you can specify the username and password of it by adding the following configuration to your `vars.yml` file.

```yaml
miniflux_admin_login: ADMIN_USERNAME_HERE
miniflux_admin_password: ADMIN_PASSWORD_HERE
```

## Usage

After running the command for installation, the Miniflux instance becomes available at the URL specified with `miniflux_hostname` and `miniflux_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/miniflux`.

To get started, open the URL with a web browser to log in. You can create additional users (admin-privileged or not) after logging in with your administrator username (`miniflux_admin_login`) and password (`miniflux_admin_password`).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-miniflux/blob/main/docs/configuring-miniflux.md#troubleshooting) on the role's documentation for details.

## Related services

- [FreshRSS](freshrss.md) — Lightweight and powerful self-hosted RSS and Atom feed aggregator
- [ReactFlux](reactflux.md) — Third-party web frontend for Miniflux, aimed at providing a more user-friendly reading experience
