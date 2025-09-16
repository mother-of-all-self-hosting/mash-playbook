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
SPDX-FileCopyrightText: 2023 Niels Bouma
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Changedetection.io

The playbook can install and configure [Changedetection.io](https://github.com/dgtlmoon/changedetection.io) for you.

Changedetection.io is a simple website change detection and restock monitoring solution.

See the project's [documentation](https://github.com/dgtlmoon/changedetection.io/blob/master/README.md) to learn what Changedetection.io does and why it might be useful to you.

For details about configuring the [Ansible role for Changedetection.io](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection/blob/main/docs/configuring-changedetection.md) online
- 📁 `roles/galaxy/changedetection/docs/configuring-changedetection.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# Changedetection.io                                                   #
#                                                                      #
########################################################################

changedetection_enabled: true

changedetection_hostname: mash.example.com
changedetection_path_prefix: /changedetection

########################################################################
#                                                                      #
# /Changedetection.io                                                  #
#                                                                      #
########################################################################
```

### Enable Playwright webdriver for advanced options (optional)

Some advanced options like using Javascript or the Visual Selector tool require an additional Playwright webdriver. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection/blob/main/docs/configuring-changedetection.md#enable-playwright-webdriver-for-advanced-options-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Changedetection.io instance becomes available at the URL specified with `changedetection_hostname` and `changedetection_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/changedetection`.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection/blob/main/docs/configuring-changedetection.md#troubleshooting) on the role's documentation for details.
