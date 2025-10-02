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

# Immich Kiosk

The playbook can install and configure [Immich Kiosk](https://immichkiosk.app) for you.

Immich Kiosk is a software for displaying photos and videos on your [Immich](https://immich.app) server in highly customizable slideshows that run in browsers and other devices.

See the project's [documentation](https://docs.immichkiosk.app) to learn what Immich Kiosk does and why it might be useful to you.

For details about configuring the [Ansible role for Immich Kiosk](https://github.com/mother-of-all-self-hosting/ansible-role-immich-kiosk), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-immich-kiosk/blob/main/docs/configuring-immich-kiosk.md) online
- 📁 `roles/galaxy/immich_kiosk/docs/configuring-immich-kiosk.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# immich_kiosk                                                         #
#                                                                      #
########################################################################

immich_kiosk_enabled: true

immich_kiosk_hostname: cyberchef.example.com

########################################################################
#                                                                      #
# /immich_kiosk                                                        #
#                                                                      #
########################################################################
```

**Note**: hosting Immich Kiosk under a subpath (by configuring the `immich_kiosk_path_prefix` variable) does not seem to be possible due to Immich Kiosk's technical limitations.

### Set the Immich's API key and URLs

It is also necessary to specify the API key and URLs of the Immich's instance. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-immich-kiosk/blob/main/docs/configuring-immich-kiosk.md#set-the-immich-instances-api-key) on the role's documentation for details.

## Usage

After running the command for installation, the Immich Kiosk instance becomes available at the URL specified with `immich_kiosk_hostname`. With the configuration above, the service is hosted at `https://cyberchef.example.com`.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-immich-kiosk/blob/main/docs/configuring-immich-kiosk.md#troubleshooting) on the role's documentation for details.
