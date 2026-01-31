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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Cinny

The playbook can install and configure [Cinny](https://github.com/ajbura/cinny) for you.

Cinny is a web client for [Matrix](https://matrix.org/), realtime communication (chat) network. It focuses primarily on simple, elegant and secure interface.

See the project's [documentation](https://github.com/cinnyapp/cinny/blob/dev/README.md) to learn what Cinny does and why it might be useful to you.

For details about configuring the [Ansible role for Cinny](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3P5L5p1gs7TGCpmhaXKUYmTJNKpi), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3P5L5p1gs7TGCpmhaXKUYmTJNKpi/tree/docs/configuring-cinny.md) online
- 📁 `roles/galaxy/cinny/docs/configuring-cinny.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> To communicate with other people on the Matrix network you need to prepare a Matrix homeserver which this client can connect to. While it is still possible to use a public homeserver with the Cinny instance, [this "matrix-docker-ansible-deploy" Ansible playbook](https://github.com/spantaleev/matrix-docker-ansible-deploy/) lets you set up Matrix services from the core ones such as a homeserver to other goodies like "bridges" on your server — it is maintained by the same team behind this MASH playbook.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# cinny                                                                #
#                                                                      #
########################################################################

cinny_enabled: true

cinny_hostname: cinny.example.com

########################################################################
#                                                                      #
# /cinny                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting Cinny under a subpath (by configuring the `cinny_path_prefix` variable) does not seem to be possible due to Cinny's technical limitations.

### Set the default homeserver URL

It is also necessary to specify the default homeserver's URL. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3P5L5p1gs7TGCpmhaXKUYmTJNKpi/tree/docs/configuring-cinny.md#set-the-default-homeserver-url) on the role's documentation for details.

## Usage

After running the command for installation, the Cinny instance becomes available at the URL specified with `cinny_hostname`. With the configuration above, the service is hosted at `https://cinny.example.com`.

To get started, open the URL with a web browser, and log in to your homeserver with the Matrix account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3P5L5p1gs7TGCpmhaXKUYmTJNKpi/tree/docs/configuring-cinny.md#troubleshooting) on the role's documentation for details.

## Related services

- [Matrix Rooms Search API](mrs.md) — Fully-featured, standalone, Matrix rooms search service
