<!--
SPDX-FileCopyrightText: 2021 foxcris
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Mosquitto

The playbook can install and configure [Mosquitto](https://mosquitto.org/) for you.

Mosquitto is a high performance, embeddable [MQTT](https://en.wikipedia.org/wiki/MQTT) broker.

The [Ansible role for Mosquitto](https://github.com/mother-of-all-self-hosting/ansible-role-mosquitto) is developed and maintained by the MASH project. For details about configuring Mosquitto, you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-mosquitto/blob/main/docs/configuring-mosquitto.md) online
- 📁 `roles/galaxy/mosquitto/docs/configuring-mosquitto.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Alternatives

[rumqttd](rumqttd.md) is another high performance, embeddable MQTT broker.
