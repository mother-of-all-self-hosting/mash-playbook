<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020 Scott Crossen
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ddclient

The playbook can install and configure [ddclient](https://ddclient.net/) for you.

ddclient is a Perl client to update dynamic DNS entries for accounts on a wide range of dynamic DNS services.

See the project's [documentation](https://ddclient.net/) to learn what ddclient does and why it might be useful to you.

For details about configuring the [Ansible role for ddclient](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md) online
- 📁 `roles/galaxy/ddclient/docs/configuring-ddclient.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ddclient                                                             #
#                                                                      #
########################################################################

ddclient_enabled: true

########################################################################
#                                                                      #
# /ddclient                                                            #
#                                                                      #
########################################################################
```

### Add configurations for dynamic DNS provider

To enable the service it is also required to add configurations for your dynamic DNS provider. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md#add-configurations-for-dynamic-dns-provider) on the role's documentation for details about what to be added. Keep in mind that certain providers may require a different configuration.

You might need to specify the endpoint to obtain IP address as well. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md#setting-the-endpoint-to-obtain-ip-address-optional) for more information.

## Usage

After running the command for installation, ddclient becomes available. Your DNS entry will be automatically updated per seconds specified to `ddclient_daemon_interval` (300 seconds by default).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md#troubleshooting) on the role's documentation for details.
