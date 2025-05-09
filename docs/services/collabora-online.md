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

# Collabora Online

The playbook can install and configure [Collabora Online Development Edition (CODE)](https://www.collaboraonline.com/code/) for you.

CODE is the development version of [Collabora Online](https://www.collaboraonline.com/), which enables you to edit office documents online with integrations such as [Nextcloud](https://nextcloud.com/office/), [OwnCloud](https://owncloud.com/), and [XWiki](https://xwiki.com/en/Blog/Collabora-Connector-Application/).

See the project's [documentation](https://www.collaboraonline.com/code/) to learn what CODE does and why it might be useful to you.

For details about configuring the [Ansible role for CODE](https://github.com/mother-of-all-self-hosting/ansible-role-collabora-online), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-collabora-online/blob/main/docs/configuring-collabora-online.md) online
- 📁 `roles/galaxy/collabora_online/docs/configuring-online.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

>[!NOTE]
> To use a CODE instance to edit office documents, it is necessary to integrate it with another software which functions as a data storage and manages access control for users. **You cannot edit the documents without such integrations.** This playbook supports installing Nextcloud. See [this page](nextcloud.md) for details about configuring it.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# collabora-online                                                     #
#                                                                      #
########################################################################

collabora_online_enabled: true

collabora_online_hostname: collabora.example.com

# A password for the admin interface, available at: https://collabora.example.com/browser/dist/admin/admin.html
# Use only alpha-numeric characters
collabora_online_environment_variable_password: ''

collabora_online_environment_variable_aliasgroup1: "https://{{ nextcloud_hostname | replace('.', '\\.') }}:443"

########################################################################
#                                                                      #
# /collabora-online                                                    #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://collabora.example.com`.


## Integrating with Nextcloud

To learn how to integrate Collabora Online with Nextcloud, see the [Collabora Online section](nextcloud.md#collabora-online) in our Nextcloud documentation.


## Admin Interface

There's an admin interface with various statistics and information at: `https://COLLABORA_ONLINE_DOMAIN/browser/dist/admin/admin.html`

Use your admin credentials for logging in:

- the default username is `admin`, as specified in `collabora_online_environment_variable_username`
- the password is the one you've specified in `collabora_online_environment_variable_password`
