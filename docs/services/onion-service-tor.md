<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Onion Service with C Tor

The playbook can install and configure [Onion Service with C Tor](https://community.torproject.org/onion-services/) with [Onimages](https://gitlab.torproject.org/tpo/onion-services/onimages) for you.

Onion Service is a service that can only be accessed over Tor.

See the project's [documentation](https://community.torproject.org/onion-services/overview/) to learn what Onion Service with C Tor does and why it might be useful to you.

For details about configuring the [Ansible role for Onion Service with C Tor](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Aznw3BPXrSbPWcARpYbk3yGy4iGQ4), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Aznw3BPXrSbPWcARpYbk3yGy4iGQ4/tree/docs/configuring-onion-service-tor.md) online
- 📁 `roles/galaxy/onion_service_tor/docs/configuring-onion-service-tor.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> Please make sure that this role is configured to set up Onion Service with [C Tor](https://gitlab.torproject.org/tpo/core/tor), not [Arti](https://gitlab.torproject.org/tpo/core/arti).

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# onion_service_tor                                                    #
#                                                                      #
########################################################################

onion_service_tor_enabled: true

########################################################################
#                                                                      #
# /onion_service_tor                                                   #
#                                                                      #
########################################################################
```

### Wire services with C Tor

You can host services of the playbook by wiring them with the `onion_service_tor_services_list` variable as below:

```yaml
onion_service_tor_services_list:
  - dir: YOUR_SERVICE_DIRECTORY_HERE
    port: VIRTUAL_PORT_NUMBER_HERE
    service: YOUR_SERVICE_NAME_HERE:YOUR_SERVICE_PORT_HERE
```

For example, you can provide [AnonymousOverflow](anonymousoverflow.md) and [Radicle Explorer](radicle-explorer.md) as Onion Service by adding the following configuration to your `vars.yml` file:

```yaml
onion_service_tor_services_list:
  - dir: "{{ anonymousoverflow_identifier }}"
    port: "{{ onion_service_tor_container_http_port }}"
    service: "{{ anonymousoverflow_identifier }}:{{ anonymousoverflow_container_http_port }}"

  - dir: "{{ radicle_explorer_identifier }}"
    port: "{{ onion_service_tor_container_http_port }}"
    service: "{{ radicle_explorer_identifier }}:{{ radicle_explorer_container_http_port }}"
```

It will by default create two directories named with values specified to `anonymousoverflow_identifier` and `radicle_explorer_identifier` inside `mash-onion-service-tor/data`, where the Onion Service key and `hostname` file are generated for each service.

Alternatively, you can completely redefine `torrc` by using `onion_service_tor_torrc_custom`, so that you can provide settings on your `torrc` file.

## Usage

After running the command for installation, the Onion Service with C Tor instance becomes available.

### Outputting Onion Service hostname

The Onion Service's hostname is written on the file named `hostname` inside a directory in `onion_service_tor_data_path`. You can output a list of the hostnames by running the playbook as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=print-hostname-onion-service-tor
```

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Aznw3BPXrSbPWcARpYbk3yGy4iGQ4/tree/docs/configuring-onion-service-tor.md#troubleshooting) on the role's documentation for details.

## Related services

- [Standalone Snowflake proxy](snowflake.md) — Help users connect to the Tor network in places where Tor is blocked
