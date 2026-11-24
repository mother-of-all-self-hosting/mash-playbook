<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024, 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LibreSpeed

The playbook can install and configure [LibreSpeed](https://librespeed.org) for you.

LibreSpeed is a self-hosted speed test, which runs in the browser and measures the connection between the client and your server.

See the project's [documentation](https://github.com/librespeed/speedtest/blob/master/README.md) to learn what LibreSpeed does and why it might be useful to you.

For details about configuring the [Ansible role for LibreSpeed](https://github.com/mother-of-all-self-hosting/ansible-role-librespeed), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-librespeed/blob/main/docs/configuring-librespeed.md) online
- 📁 `roles/galaxy/librespeed/docs/configuring-librespeed.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# librespeed                                                           #
#                                                                      #
########################################################################

librespeed_enabled: true

librespeed_hostname: librespeed.example.com

########################################################################
#                                                                      #
# /librespeed                                                          #
#                                                                      #
########################################################################
```

As most of the necessary settings for the role have been taken care of by the playbook, you can enable LibreSpeed on your server with this minimum configuration.

See the role's documentation for details about configuring LibreSpeed per your preference (such as [customizing the appearance](https://github.com/mother-of-all-self-hosting/ansible-role-librespeed/blob/main/docs/configuring-librespeed.md#customize-the-appearance-optional) and [saving test results](https://github.com/mother-of-all-self-hosting/ansible-role-librespeed/blob/main/docs/configuring-librespeed.md#save-test-results-optional)).

>[!WARNING]
> By default anyone who can reach the instance can run the test, which uses up as much of your server's bandwidth as possible. To require a login, you can enable HTTP Basic authentication (see the `librespeed_container_labels_traefik_middleware_basic_auth_*` variables on the role's [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-librespeed/blob/main/defaults/main.yml)) or put the service behind an authentication service like [Tinyauth](../tinyauth/README.md).

## Usage

After running the command for installation, the LibreSpeed instance becomes available at the URL specified with `librespeed_hostname`. With the configuration above, the service is hosted at `https://librespeed.example.com`.

To use it, open the URL on the browser and start the test. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-librespeed/blob/main/docs/configuring-librespeed.md#avoiding-inaccurate-results) on the role's documentation for what can make the results inaccurate.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-librespeed/blob/main/docs/configuring-librespeed.md#troubleshooting) on the role's documentation for details.
