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

# FMD Server

The playbook can install and configure [FMD Server](https://gitlab.com/fmd-foss/fmd-server) (aka. FindMyDeviceServer) for you.

FMD Server is the official server for [FMD (FindMyDevice)](https://gitlab.com/fmd-foss/fmd-android), which allows you to locate, ring, wipe and issue other commands to your Android device when it is lost.

See the project's [documentation](https://gitlab.com/fmd-foss/fmd-server/-/blob/master/README.md) to learn what FMD Server does and why it might be useful to you.

For details about configuring the [Ansible role for FMD Server](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server/blob/main/docs/configuring-fmd-server.md) online
- 📁 `roles/galaxy/fmd_server/docs/configuring-fmd-server.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# fmd_server                                                           #
#                                                                      #
########################################################################

fmd_server_enabled: true

fmd_server_hostname: fmd.example.com

########################################################################
#                                                                      #
# /fmd_server                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting FMD Server under a subpath (by configuring the `fmd_server_path_prefix` variable) does not seem to be possible due to FMD Server's technical limitations.

### Set the path for storing a database file on the host

For a persistent storage for a database file, you need to add a Docker volume to mount in the container to share it with the host machine.

To add the volume, prepare a directory on the host machine and add the following configuration to your `vars.yml` file:

```yaml
fmd_server_database_path: /path/on/the/host
```

Make sure permissions of the directory specified to `/path/on/the/host`.

### Set a registration token (optional)

With the default setting, the instance will be public and open to registration by anyone.

To make it private and have it require a token for registration, set it by adding the following configuration to your `vars.yml` file. Make sure to replace `YOUR_TOKEN_HERE` with your own value. Generating a strong token (e.g. `pwgen -s 64 1`) is recommended.

```yaml
fmd_server_config_registrationtoken: YOUR_TOKEN_HERE
```

## Usage

After running the command for installation, FMD Server becomes available at the specified hostname like `https://fmd.example.com`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server/blob/main/docs/configuring-fmd-server.md#usage) on the role's documentation for details about how to set up the client (FMD).

>[!NOTE]
> As sending commands from FMD Server to your device requires a UnifiedPush Distributor application, you might be interested in self-hosting a [ntfy](ntfy.md) Push Server along with it.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server/blob/main/docs/configuring-fmd-server.md#troubleshooting) on the role's documentation for details.
