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

# FindMyDeviceServer

The playbook can install and configure [FindMyDeviceServer](https://gitlab.com/Nulide/findmydeviceserver) for you.

FindMyDeviceServer is the official server for [FindMyDevice (FMD)](https://gitlab.com/Nulide/findmydevice), which allows you to locate, ring, wipe and issue other commands to your Android device when it is lost.

See the project's [documentation](https://gitlab.com/Nulide/findmydeviceserver/-/blob/master/README.md) to learn what FindMyDeviceServer does and why it might be useful to you.

For details about configuring the [Ansible role for FindMyDeviceServer](https://github.com/mother-of-all-self-hosting/ansible-role-findmydeviceserver), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-findmydeviceserver/blob/main/docs/configuring-findmydeviceserver.md) online
- 📁 `roles/galaxy/findmydeviceserver/docs/configuring-findmydeviceserver.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# findmydeviceserver                                                   #
#                                                                      #
########################################################################

findmydeviceserver_enabled: true

findmydeviceserver_hostname: fmd.example.com

########################################################################
#                                                                      #
# /findmydeviceserver                                                  #
#                                                                      #
########################################################################
```

**Note**: hosting FindMyDeviceServer under a subpath (by configuring the `findmydeviceserver_path_prefix` variable) does not seem to be possible due to FindMyDeviceServer's technical limitations.

### Set the path for storing a database file on the host

For a persistent storage for a database file, you need to add a Docker volume to mount in the container to share it with the host machine.

To add the volume, prepare a directory on the host machine and add the following configuration to your `vars.yml` file:

```yaml
findmydeviceserver_database_path: /path/on/the/host
```

Make sure permissions of the directory specified to `/path/on/the/host`.

### Set a registration token (optional)

With the default setting, the instance will be public and open to registration by anyone.

To make it private and have it require a token for registration, set it by adding the following configuration to your `vars.yml` file. Make sure to replace `YOUR_TOKEN_HERE` with your own value. Generating a strong token (e.g. `pwgen -s 64 1`) is recommended.

```yaml
findmydeviceserver_config_registrationtoken: YOUR_TOKEN_HERE
```

## Usage

After running the command for installation, FindMyDeviceServer becomes available at the specified hostname like `https://fmd.example.com`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-findmydeviceserver/blob/main/docs/configuring-findmydeviceserver.md#usage) on the role's documentation for details about how to set up the client (FindMyDevice).

>[!NOTE]
> As sending commands from FindMyDeviceServer to your device requires a UnifiedPush Distributor application, you might be interested in self-hosting a [ntfy](ntfy.md) Push Server along with it.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-findmydeviceserver/blob/main/docs/configuring-findmydeviceserver.md#troubleshooting) on the role's documentation for details.
