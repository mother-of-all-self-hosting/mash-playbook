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
SPDX-FileCopyrightText: 2024 Tiz
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

- [Immich](immich.md)
- (optional) [Traefik](traefik.md) — a reverse-proxy server for exposing Immich Kiosk publicly

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# immich_kiosk                                                         #
#                                                                      #
########################################################################

immich_kiosk_enabled: true

########################################################################
#                                                                      #
# /immich_kiosk                                                        #
#                                                                      #
########################################################################
```

### Set the Immich's API key and URLs

It is also necessary to specify the API key and URLs of the Immich's instance. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-immich-kiosk/blob/main/docs/configuring-immich-kiosk.md#set-the-immich-instances-api-key) on the role's documentation for details.

### Expose the instance publicly (optional)

By default, the Immich Kiosk is not exposed externally, as it is mainly intended to be used in the internal network, connected to the Immich server.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which Immich Kiosk is served.
immich_kiosk_hostname: "immichkiosk.example.com"

immich_kiosk_container_labels_traefik_enabled: true
```

>[!NOTE]
>
> - Hosting Immich Kiosk under a subpath (by configuring the `immich_kiosk_path_prefix` variable) does not seem to be possible due to Immich Kiosk's technical limitations.
> - When exposing the instance, it is recommended to consider to set a password (see [this section](https://docs.immichkiosk.app/configuration/additional-options/#password) for the necessary configuration) as well as enable a service for authentication such as [authentik](authentik.md) and [Tinyauth](tinyauth.md) based on your use-case.

## Usage

After running the command for installation, Immich Kiosk becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the URL specified with `immich_kiosk_hostname`. With the configuration above, the service is hosted at `https://immichkiosk.example.com`.

To get started, refer to [the documentation](https://docs.immichkiosk.app/guides/digital-picture-frame-immich-kiosk-old-tablet/) and other pages for guides about how to display pictures on devices.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-immich-kiosk/blob/main/docs/configuring-immich-kiosk.md#troubleshooting) on the role's documentation for details.
