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

findmydeviceserver_hostname: findmydeviceserver.example.com

########################################################################
#                                                                      #
# /findmydeviceserver                                                  #
#                                                                      #
########################################################################
```

**Note**: hosting FindMyDeviceServer under a subpath (by configuring the `findmydeviceserver_path_prefix` variable) is technically possible but not recommended, as most of the functions do not work as expected due to FindMyDeviceServer's technical limitations (pages and resources are not correctly loaded, and links are broken).

### Configure instance and user settings (optional)

There are various options for the instance and user settings. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-findmydeviceserver/blob/main/docs/configuring-findmydeviceserver.md#configure-instance-and-user-settings-optional) on the role's documentation for details.

## Usage

After running the command for installation, FindMyDeviceServer becomes available at the specified hostname like `https://findmydeviceserver.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to FindMyDeviceServer.

If you would like to make your instance public so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://github.com/findmydeviceserver-org/findmydeviceserver-instances) to add yours to the list, which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)). See [here](https://github.com/findmydeviceserver-org/findmydeviceserver-instances/blob/main/README.md) for details about how to do so.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-findmydeviceserver/blob/main/docs/configuring-findmydeviceserver.md#troubleshooting) on the role's documentation for details.
