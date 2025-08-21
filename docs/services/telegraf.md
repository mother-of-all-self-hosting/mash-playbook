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

# Telegraf

The playbook can install and configure [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) for you.

Telegraf is an open source server agent to help you collect metrics from your stacks, sensors, and systems.

See the project's [documentation](https://docs.influxdata.com/telegraf/v1/) to learn what Telegraf does and why it might be useful to you.

For details about configuring the [Ansible role for Telegraf](https://github.com/mother-of-all-self-hosting/ansible-role-telegraf), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-telegraf/blob/main/docs/configuring-telegraf.md) online
- 📁 `roles/galaxy/telegraf/docs/configuring-telegraf.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# telegraf                                                             #
#                                                                      #
########################################################################

telegraf_enabled: true

########################################################################
#                                                                      #
# /telegraf                                                            #
#                                                                      #
########################################################################
```

### Set variables for connecting to an InfluxDB instance (optional)

The Telegraf instance can be configured to collect and write metrics to [InfluxDB](https://www.influxdata.com/) or other outputs. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-telegraf/blob/main/docs/configuring-telegraf.md#set-variables-for-connecting-to-an-influxdb-instance-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Telegraf instance becomes available.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-telegraf/blob/main/docs/configuring-telegraf.md#troubleshooting) on the role's documentation for details.
