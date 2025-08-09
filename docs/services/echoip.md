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
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# echoip

The playbook can install and configure [echoip](https://github.com/mpolden/echoip) for you.

echoip is simple service for looking up your IP address, which powers [ifconfig.co](https://ifconfig.co).

See the project's [documentation](https://github.com/mpolden/echoip/blob/master/README.md) to learn what echoip does and why it might be useful to you.

For details about configuring the [Ansible role for echoip](https://github.com/mother-of-all-self-hosting/ansible-role-echoip), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-echoip/blob/main/docs/configuring-echoip.md) online
- 📁 `roles/galaxy/echoip/docs/configuring-echoip.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# echoip                                                               #
#                                                                      #
########################################################################

echoip_enabled: true

echoip_hostname: echoip.example.com

########################################################################
#                                                                      #
# /echoip                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the echoip instance becomes available at the URL specified with `echoip_hostname`. With the configuration above, the service is hosted at `https://echoip.example.com`.

You can use the echoip instance by running a command as below:

```sh
curl https://echoip.example.com
```

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-echoip/blob/main/docs/configuring-echoip.md#troubleshooting) on the role's documentation for details.
