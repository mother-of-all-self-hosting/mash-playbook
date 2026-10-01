<!--
SPDX-FileCopyrightText: 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 XHawk87
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Minecraft Server on Docker (Java Edition)

The playbook can install and configure [itzg docker-minecraft server](https://docker-minecraft-server.readthedocs.io) for you.

Minecraft is a first-person open-world procedurally-generated voxel-based sandbox game with RPG elements. The Docker image which this playbook installs provides a Minecraft Server which will automatically download the latest stable version at startup.

See the project's [documentation](https://docker-minecraft-server.readthedocs.io/en/latest/) to learn what it does and why it might be useful to you.

> [!WARNING]
> itzg docker-minecraft server is published under the Apache-2.0 license, however Minecraft itself is proprietary software, and by using this role you are agreeing to the [EULA](https://www.minecraft.net/en-us/eula). Know your rights!

The [Ansible role for Minecraft Server](https://github.com/mother-of-all-self-hosting/ansible-role-minecraft) is developed and maintained by the MASH project. For details about configuring Minecraft Server, you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-minecraft/blob/main/docs/configuring-minecraft.md) online
- 📁 `roles/galaxy/minecraft/docs/configuring-minecraft.md` locally, if you have [fetched the Ansible roles](../installing.md)
