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
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2025 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Matomo

The playbook can install and configure [Matomo](https://matomo.org/) (formerly Piwik) for you.

Matomo is a leading open-source web analytics platform that gives you full data ownership.

See the project's [documentation](https://matomo.org/guides/) to learn what Matomo does and why it might be useful to you.

For details about configuring the [Ansible role for Matomo](https://github.com/mother-of-all-self-hosting/ansible-role-matomo), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-matomo/blob/main/docs/configuring-matomo.md) online
- 📁 `roles/galaxy/matomo/docs/configuring-matomo.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- MySQL / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# matomo                                                               #
#                                                                      #
########################################################################

matomo_enabled: true

matomo_hostname: matomo.example.com

########################################################################
#                                                                      #
# /matomo                                                              #
#                                                                      #
########################################################################
```

### Enable MariaDB

Matomo requires a MySQL-compatible database to work. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`.

Refer to [this page](mariadb.md) for the instruction to enable it.

## Usage

After running the command for installation, the Matomo instance becomes available at the URL specified with `matomo_hostname`. With the configuration above, the service is hosted at `https://matomo.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard where you can

- Create the administrator account
- Configure your first website to track
- Get the tracking code for your website

>[!NOTE]
> On the step three (Database Setup), please make sure to select `MariaDB` for the database engine instead of `MySQL`.

After finishing installation, you can log in to the service with the administrator account. If you have added the tracking code to your website, the Matomo instance should have started collecting analytics data.

## Related services

- [OxiTraffic](oxitraffic.md) — Self-hosted, simple and privacy respecting website traffic tracker
- [Plausible Analytics](plausible.md) — Intuitive, lightweight and open source web analytics
