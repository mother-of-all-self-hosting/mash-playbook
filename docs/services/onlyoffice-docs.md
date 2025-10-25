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

# ONLYOFFICE Docs

The playbook can install and configure [ONLYOFFICE Docs](https://www.collaboraonline.com/code/) for you.

ONLYOFFICE Docs is the development version of [Collabora Online](https://www.collaboraonline.com/), which enables you to edit office documents online with integrations such as [Nextcloud](https://nextcloud.com/office/), [OwnCloud](https://owncloud.com/), and [XWiki](https://xwiki.com/en/Blog/Collabora-Connector-Application/).

See the project's [documentation](https://www.collaboraonline.com/code/) to learn what ONLYOFFICE Docs does and why it might be useful to you.

For details about configuring the [Ansible role for ONLYOFFICE Docs](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3kozTn4Kn5eJtgJQj1aCFUpqxW5Y), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3kozTn4Kn5eJtgJQj1aCFUpqxW5Y/tree/docs/configuring-onlyoffice-docs.md) online
- 📁 `roles/galaxy/onlyoffice_docs/docs/configuring-onlyoffice-docs.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

>[!NOTE]
> To use an ONLYOFFICE Docs instance to edit office documents, it is necessary to integrate it with another software which functions as a data storage and manages access control for users. **You cannot edit the documents without such integrations.** This playbook supports installing Nextcloud. See [this page](nextcloud.md) for details about configuring it.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# onlyoffice_docs                                                      #
#                                                                      #
########################################################################

onlyoffice_docs_enabled: true

onlyoffice_docs_hostname: onlyoffice.example.com

# A password for the admin interface, available at: https://collabora.example.com/browser/dist/admin/admin.html
# Use only alphanumeric characters
onlyoffice_docs_environment_variable_password: ''

########################################################################
#                                                                      #
# /onlyoffice_docs                                                     #
#                                                                      #
########################################################################
```

### Integrate ONLYOFFICE Docs with Nextcloud (optional)

To use an ONLYOFFICE Docs instance to edit office documents, you need to integrate it with a File Sync and Share solution that implements the WOPI (*Web Application Open Platform Interface*) protocol, such as Nextcloud.

By default, this playbook is configured to automatically integrate the ONLYOFFICE Docs with the Nextcloud instance which this playbook manages, if both of them are enabled.

>[!NOTE]
> For details, see [this section about the integration](nextcloud.md#collabora-online-development-edition) on our Nextcloud documentation.

## Usage

After running the command for installation, the ONLYOFFICE Docs becomes available at the URL specified with `onlyoffice_docs_hostname`. With the configuration above, the service is hosted at `https://onlyoffice.example.com`.

### Admin Interface

There's an admin interface with various statistics and information at: `https://collabora.example.com/browser/dist/admin/admin.html`

Use your admin credentials for logging in:

- the default username is `admin`, as specified with `onlyoffice_docs_environment_variable_username`
- the password is the one you've specified with `onlyoffice_docs_environment_variable_password`

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3kozTn4Kn5eJtgJQj1aCFUpqxW5Y/tree/docs/configuring-onlyoffice-docs.md#troubleshooting) on the role's documentation for details.

## Related services

- [Nextcloud](nextcloud.md) — Self-hosted collaboration solution for tens of millions of users at thousands of organizations across the globe
