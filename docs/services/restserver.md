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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Rest Server

The playbook can install and configure [Rest Server](https://github.com/restic/rest-server) for you.

Rest Server is an HTTP server that implements restic's REST backend API to backup data remotely, using restic backup client via the `rest:` URL.

See the project's [documentation](https://github.com/restic/rest-server/blob/master/README.md) to learn what Rest Server does and why it might be useful to you.

For details about configuring the [Ansible role for Rest Server](https://radicle.network/nodes/iris.radicle.network/rad%3Azi4z5FpzySQ1kRqVpqcTkEfnXrD9), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Azi4z5FpzySQ1kRqVpqcTkEfnXrD9/tree/docs/configuring-restserver.md) online
- 📁 `roles/galaxy/restserver/docs/configuring-restserver.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# restserver                                                           #
#                                                                      #
########################################################################

restserver_enabled: true

restserver_hostname: restserver.example.com

########################################################################
#                                                                      #
# /restserver                                                          #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

The HTTP Basic authentication on Traefik is enabled for the web interface by default, considering the nature of the service. See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Azi4z5FpzySQ1kRqVpqcTkEfnXrD9/tree/docs/configuring-restserver.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up or disable it.

## Usage

After running the command for installation, the Rest Server instance becomes available at the URL specified with `restserver_hostname`. With the configuration above, the service is hosted at `https://restserver.example.com`.

Refer to [this section](https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#rest-server) on the official documentation for details about how to prepare a new repository.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Azi4z5FpzySQ1kRqVpqcTkEfnXrD9/tree/docs/configuring-restserver.md#troubleshooting) on the role's documentation for details.

## Related services

- [BorgBackup with borgmatic](backup-borg.md) — Deduplicating backup program with optional compression and encryption
- [Borg Web UI](borg-ui.md) — Unofficial web interface for BorgBackup
- [Duplicati](duplicati.md) — Backup software that securely stores encrypted, incremental, compressed backups on local storage, cloud storage services and remote file servers
