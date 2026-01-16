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

# Onion Service with C Tor

The playbook can install and configure [Onion Service with C Tor](https://github.com/mpolden/onion-service-tor) for you.

Onion Service with C Tor is simple service for looking up your IP address, which powers [ifconfig.co](https://ifconfig.co).

See the project's [documentation](https://github.com/mpolden/onion-service-tor/blob/master/README.md) to learn what Onion Service with C Tor does and why it might be useful to you.

For details about configuring the [Ansible role for Onion Service with C Tor](https://github.com/mother-of-all-self-hosting/ansible-role-onion-service-tor), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-onion-service-tor/blob/main/docs/configuring-onion-service-tor.md) online
- 📁 `roles/galaxy/onion_service_tor/docs/configuring-onion-service-tor.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# onion_service_tor                                                    #
#                                                                      #
########################################################################

onion_service_tor_enabled: true

onion_service_tor_hostname: onion-service-tor.example.com

########################################################################
#                                                                      #
# /onion_service_tor                                                   #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Onion Service with C Tor instance becomes available at the URL specified with `onion_service_tor_hostname`. With the configuration above, the service is hosted at `https://onion_service_tor.example.com`.

You can use the Onion Service with C Tor instance by running a command as below:

```sh
curl https://onion-service-tor.example.com
```

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-onion-service-tor/blob/main/docs/configuring-onion-service-tor.md#troubleshooting) on the role's documentation for details.
