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

# Radicle HTTP Daemon

The playbook can install and configure the Radicle HTTP Daemon (`radicle-httpd`) for you.

The Radicle HTTP Daemon is the network daemon based on [Heartwood](https://app.radicle.xyz/nodes/seed.radicle.xyz/rad%3Az3gqcJUoA1n9HaHKufZs5FCSGazv5), the third iteration of the Radicle Protocol, which powers the [Radicle](https://radicle.xyz/) network, a peer-to-peer code collaboration stack built on Git.

In Radicle, while all nodes contribute to the network by seeding data to others, running `radicle-httpd` as the *seed node* on a highly available server can help to keep the peer-to-peer network resilient and healthy.

See the project's [documentation](https://radicle.xyz/guides/seeder#introduction) to learn what `radicle-httpd` does and why it might be useful to you.

For details about configuring the [Ansible role for Radicle HTTP Daemon](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az28JTUhepmbS3hLZyUeEvXeqk9QW5), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az28JTUhepmbS3hLZyUeEvXeqk9QW5/tree/docs/configuring-radicle-httpd.md) online
- 📁 `roles/galaxy/radicle_httpd/docs/configuring-radicle-httpd.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

You may need to open some ports to your server, if you use another firewall in front of the server. Refer to [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az28JTUhepmbS3hLZyUeEvXeqk9QW5/tree/docs/configuring-radicle-httpd.md#prerequisites) to check which ones to be configured.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# radicle_httpd                                                        #
#                                                                      #
########################################################################

radicle_httpd_enabled: true

radicle_httpd_hostname: seed.example.com

########################################################################
#                                                                      #
# /radicle_httpd                                                       #
#                                                                      #
########################################################################
```

## Usage

### Updating configuration

After running the command for installation, run the command below to update basic settings like `externalAddresses`, so that nodes outside of the internal network can connect to the seed node:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=adjust-config-radicle-httpd
```

The Radicle HTTP Daemon instance then becomes available at the hostname specified with `radicle_httpd_hostname` and `radicle_httpd_container_node_port`. With the configuration above, it is hosted at `seed.example.com:8776`.

>[!NOTE]
> `radicle-httpd` cannot be accessed via HTTP. For browsing repositories on a web browser, it is necessary to set up the HTTP Daemon (`radicle-httpd`). See [this section](https://radicle.xyz/guides/seeder#running-the-http-daemon) on the documentation for details.

Please note that the default seeding policy is *selective* one, meaning that the node will ignore all repositories, except the ones which the node's operator explicitly allows to be seeded.

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az28JTUhepmbS3hLZyUeEvXeqk9QW5/tree/docs/configuring-radicle-httpd.md#usage) on the role's documentation for details about updating settings including the seeding policy.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az28JTUhepmbS3hLZyUeEvXeqk9QW5/tree/docs/configuring-radicle-httpd.md#troubleshooting) on the role's documentation for details.
