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
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# transfer.sh

The playbook can install and configure [transfer.sh](https://github.com/dutchcoders/transfer.sh) for you.

transfer.sh is a tool for file sharing with the command-line.

See the project's [documentation](https://github.com/dutchcoders/transfer.sh/blob/main/README.md) to learn what transfer.sh does and why it might be useful to you.

For details about configuring the [Ansible role for transfer.sh](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3baazpMjGxvdYmB7RTqr5WnrSRke), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3baazpMjGxvdYmB7RTqr5WnrSRke/tree/docs/configuring-transfersh.md) online
- 📁 `roles/galaxy/transfersh/docs/configuring-transfer.sh.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# transfer.sh                                                          #
#                                                                      #
########################################################################

transfersh_enabled: true

transfersh_hostname: transfersh.example.com

########################################################################
#                                                                      #
# /transfer.sh                                                         #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the transfer.sh instance becomes available at the URL specified with `transfersh_hostname`. With the configuration above, the service is hosted at `https://transfersh.example.com`.

You can upload a file to the transfer.sh instance by running a command as below:

```sh
curl -v --upload-file ./hello.txt https://transfersh.example.com/hello.txt
```

See [this section](https://github.com/dutchcoders/transfer.sh/blob/main/README.md#usage) on the documentation for details about its usage.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3baazpMjGxvdYmB7RTqr5WnrSRke/tree/docs/configuring-transfersh.md#troubleshooting) on the role's documentation for details.
