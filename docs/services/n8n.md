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
SPDX-FileCopyrightText: 2023 kinduff
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# n8n

The playbook can install and configure [n8n](https://n8n.io/) for you.

n8n is a workflow automation tool for technical people.

See the project's [documentation](https://docs.n8n.io/) to learn what n8n does and why it might be useful to you.

For details about configuring the [Ansible role for n8n](https://github.com/mother-of-all-self-hosting/ansible-role-n8n), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-n8n/blob/main/docs/configuring-n8n.md) online
- 📁 `roles/galaxy/actual/docs/configuring-actual.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!WARNING]
> n8n is licensed under [Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md). Because we had discouraged using [Redis](redis.md) as it was provided under "source available" model (note: Redis has retracted its stance in the end and since version 8.0 it was started to be released under multiple licenses, one of which is AGPL-3.0), we do not encourage using n8n either on the same ground.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# n8n                                                                  #
#                                                                      #
########################################################################

n8n_enabled: true

n8n_hostname: mash.example.com
n8n_path_prefix: /n8n

########################################################################
#                                                                      #
# /n8n                                                                 #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the n8n instance becomes available at the URL specified with `n8n_hostname` and `n8n_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/n8n`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-n8n/blob/main/docs/configuring-n8n.md#troubleshooting) on the role's documentation for details.
