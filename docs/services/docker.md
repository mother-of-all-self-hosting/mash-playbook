<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Docker

This playbook installs [Docker](https://www.docker.com/) by default, because all services require it.

To disable Docker installation (and install Docker yourself in another way), use: `mash_playbook_docker_installation_enabled: false`
