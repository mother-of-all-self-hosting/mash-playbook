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
SPDX-FileCopyrightText: 2024 MASH project contributors
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# CouchDB

The playbook can install and configure [CouchDB](https://couchdb.apache.org/) for you.

CouchDB is a document-oriented NoSQL database which uses JSON to store data.

See the project's [documentation](https://docs.couchdb.org/en/stable/) to learn what CouchDB does and why it might be useful to you.

For details about configuring the [Ansible role for CouchDB](https://github.com/mother-of-all-self-hosting/ansible-role-couchdb), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-couchdb/blob/main/docs/configuring-couchdb.md) online
- 📁 `roles/galaxy/couchdb/docs/configuring-couchdb.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — a reverse-proxy server for exposing CouchDB publicly

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# couchdb                                                              #
#                                                                      #
########################################################################

couchdb_enabled: true

########################################################################
#                                                                      #
# /couchdb                                                             #
#                                                                      #
########################################################################
```

### Specify server administrator's username and password

You also need to specify a server administrator's login credential. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-couchdb/blob/main/docs/configuring-couchdb.md#specify-server-administrators-username-and-password) on the role's documentation for details.

>[!NOTE]
> CouchDB requires a server administrator account to start. If one has not been created, CouchDB will print an error message and terminate.

### Expose the instance publicly (optional)

By default, the CouchDB instance is not exposed externally, as it is mainly intended to be used in the internal network.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which CouchDB is served.
couchdb_hostname: "couchdb.example.com"
```

**Note**: hosting CouchDB under a subpath (by configuring the `couchdb_path_prefix` variable) does not seem to be possible due to CouchDB's technical limitations.

## Usage

After running the command for installation, CouchDB becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the URL specified with `couchdb_hostname`. With the configuration above, the service is hosted at `https://couchdb.example.com`.

### Creating users

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-couchdb/blob/main/docs/configuring-couchdb.md#creating-users) on the role's documentation about how to create users (administrators and normal users).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-couchdb/blob/main/docs/configuring-couchdb.md#troubleshooting) on the role's documentation for details.
