<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Gitea

[Gitea](https://gitea.io/) is a painless self-hosted Git service. You may also wish to look into [Forgejo](https://forgejo.org/) — a fork of Gitea that this playbook also [supports](forgejo.md).

> [!WARNING]
> [Gitea is Open Core](https://codeberg.org/forgejo/discussions/issues/102) and your interests may be better served by using and supporting [Forgejo](forgejo.md) instead. See the [Comparison with Gitea](https://forgejo.org/compare-to-gitea/) page for more information. You may also wish to see our [Migrating from Gitea](forgejo.md#migrating-from-gitea) guide.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gitea                                                                #
#                                                                      #
########################################################################

gitea_enabled: true

# Gitea uses port 22 by default.
# We recommend that you move your regular SSH server to another port,
# and stick to this default.
#
# If you wish to use another port, uncomment the variable below
# and adjust the port as you see fit.
# gitea_ssh_port: 222

gitea_hostname: mash.example.com
gitea_path_prefix: /gitea

########################################################################
#                                                                      #
# /gitea                                                               #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Gitea instance becomes available at the URL specified with `gitea_hostname` and `gitea_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/gitea`.

To get started, open the URL with a web browser, and follow the set up wizard where you can create your admin user and configure the service.

## Recommended other services

You may also wish to look into [Woodpecker CI](woodpecker-ci.md), which can integrate nicely with Gitea.
