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

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# OxiTraffic

The playbook can install and configure [OxiTraffic](https://codeberg.org/mo8it/oxitraffic) for you.

OxiTraffic is a self-hosted, simple and privacy respecting website traffic tracker.

See the project's [documentation](https://codeberg.org/mo8it/oxitraffic/src/branch/main/README.md) to learn what OxiTraffic does and why it might be useful to you.

For details about configuring the [Ansible role for OxiTraffic](https://github.com/mother-of-all-self-hosting/ansible-role-oxitraffic), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-oxitraffic/blob/main/docs/configuring-oxitraffic.md) online
- 📁 `roles/galaxy/oxitraffic/docs/configuring-oxitraffic.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# oxitraffic                                                           #
#                                                                      #
########################################################################

oxitraffic_enabled: true

oxitraffic_hostname: oxitraffic.example.com

########################################################################
#                                                                      #
# /oxitraffic                                                          #
#                                                                      #
########################################################################
```

### Set the website hostname

You also need to set the hostname of the website, on which the OxiTraffic instance counts visits, as below:

```yaml
oxitraffic_tracked_origin: https://example.com
```

Replace `https://example.com` with the hostname of your website.

## Usage

After running the command for installation, the OxiTraffic instance becomes available at the URL specified with `oxitraffic_hostname`. With the configuration above, the service is hosted at `https://oxitraffic.example.com`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-oxitraffic/blob/main/docs/configuring-oxitraffic.md#usage) on the role's documentation for details about how to use the service.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-oxitraffic/blob/main/docs/configuring-oxitraffic.md#troubleshooting) on the role's documentation for details.

## Related services

- [Matomo](matomo.md) — Free and open source web analytics platform
- [Plausible Analytics](plausible.md) — Intuitive, lightweight and open source web analytics
