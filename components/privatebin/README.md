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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024, 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# PrivateBin

The playbook can install and configure [PrivateBin](https://privatebin.info) for you.

PrivateBin is a minimalist, open-source online pastebin where the server has zero knowledge of pasted data.

See the project's [documentation](https://github.com/PrivateBin/PrivateBin/tree/master/doc) to learn what PrivateBin does and why it might be useful to you.

For details about configuring the [Ansible role for PrivateBin](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az47v1S9DRcEtm2dgKwZZs4YgoLRgF), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az47v1S9DRcEtm2dgKwZZs4YgoLRgF/tree/docs/configuring-privatebin.md) online
- 📁 `roles/galaxy/privatebin/docs/configuring-privatebin.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) / MySQL / [MariaDB](../mariadb/README.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](../traefik/README.md) reverse-proxy server
- (optional) [YOURLS](../yourls/README.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# privatebin                                                           #
#                                                                      #
########################################################################

privatebin_enabled: true

privatebin_hostname: mash.example.com
privatebin_path_prefix: /bin

########################################################################
#                                                                      #
# /privatebin                                                          #
#                                                                      #
########################################################################
```

### Configure a storage for pastes (optional)

PrivateBin instance requires a storage backend to work. Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az47v1S9DRcEtm2dgKwZZs4YgoLRgF/tree/docs/configuring-privatebin.md#configure-a-storage-for-pastes) on the role's documentation for details about how to configure storages.

>[!NOTE]
> If you have not disabled Postgres explicitly with this playbook, the storage backend for your existing installation is most likely to be `postgres`.

### Configure a URL shortener (optional)

It is possible to have the PrivateBin instance use a URL shortener such as Bit.ly and a [YOURLS](https://yourls.org) instance, so that users can shorten a URL of a paste with it. **It is recommended to use a self-hosted shortener only and set a password to a paste, as the shortener will leak the paste's encryption key.**

YOURLS is available on the playbook. Refer to [here](../yourls/README.md) for details about how to install it.

💡 **Notes**

- YOURLS requires a MariaDB instance (refer to [this page](../mariadb/README.md) for details about configuring it with the playbook); if PostgreSQL is going to be used for PrivateBin (or other services), you need to use both of them.
- If you are going to install PrivateBin and YOURLS at the same time, **you need to complete installation of YOURLS at first**. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-yourls/blob/main/docs/configuring-yourls.md#usage) on the role's documentation for the instruction to set it up.

#### Use a private YOURLS instance with API access key

If you are using the private YOURLS instance, you might probably want to disallow a third party to use it without credentials. You can configure authentication by adding the following configuration to your `vars.yml` file:

```yaml
privatebin_config_yourlsapi_enabled: true

# Set the "signature" (access key) issued by the YOURLS instance for using the account
privatebin_config_yourlsapi_signature: ''

# Set URL of the YOURLS instance's API, called to shorten a paste URL
privatebin_config_yourlsapi_url: https://yourls.example.com/yourls-api.php
```

You can find the "signature" and API's URL on the "Tools" page of the YOURLS instance.

## Usage

After running the command for installation, the PrivateBin instance becomes available at the URL specified with `privatebin_hostname` and `privatebin_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/bin`.

## Troubleshooting

Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az47v1S9DRcEtm2dgKwZZs4YgoLRgF/tree/docs/configuring-privatebin.md#troubleshooting) on the role's documentation for details.

## Related services

- [Opengist](../opengist/README.md) — Pastebin powered by Git
