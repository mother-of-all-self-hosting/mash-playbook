<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
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
SPDX-FileCopyrightText: 2025 Nicola Murino

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# InfluxDB

>[!NOTE]
> On this playbook, InfluxDB is implemented with [ansible-role-influxdb](https://github.com/mother-of-all-self-hosting/ansible-role-influxdb). The role is configured to install [InfluxDB OSS v2](https://docs.influxdata.com/influxdb/v2/). Though [InfluxDB 3 Core](https://docs.influxdata.com/influxdb3/core/) is open source, it is **not** a replacement for OSS v2. [InfluxDB 3 Enterprise](https://docs.influxdata.com/influxdb3/enterprise/) can replace OSS v2, but it is proprietary and we will not support it.

The playbook can install and configure [InfluxDB](https://www.influxdata.com/) for you.

InfluxDB is a self-hosted time-series database.

See the project's [documentation](https://github.com/docker-library/docs/blob/master/influxdb/README.md) to learn what InfluxDB does and why it might be useful to you.

For details about configuring the [Ansible role for Firezone](https://github.com/mother-of-all-self-hosting/ansible-role-influxdb), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-influxdb/blob/main/docs/configuring-influxdb.md) online
- 📁 `roles/galaxy/influxdb/docs/configuring-influxdb.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# influxdb                                                             #
#                                                                      #
########################################################################

influxdb_enabled: true

influxdb_hostname: influxdb.example.com

########################################################################
#                                                                      #
# /influxdb                                                            #
#                                                                      #
########################################################################
```

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-influxdb/blob/main/docs/configuring-influxdb.md#adjusting-the-playbook-configuration) on the role's documentation for other optional settings such as configuring the initial user with the playbook.

## Usage

After running the command for installation, the InfluxDB instance becomes available at the URL specified with `influxdb_hostname`. With the configuration above, the service is hosted at `https://influxdb.example.com`.

To get started, open the URL with a web browser, and log in to the service if `influxdb_init` is set to `true` (or configure the first user if it is not).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-influxdb/blob/main/docs/configuring-influxdb.md#troubleshooting) on the role's documentation for details.

## Related services

- [Telegraf](telegraf.md) — Open source server agent to collect metrics from your stacks, sensors, and systems
