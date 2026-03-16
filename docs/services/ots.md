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

# OTS

The playbook can install and configure [OTS](https://ots.fyi/) for you.

OTS is a one-time-secret sharing platform.

See the project's [documentation](https://github.com/Luzifer/ots/blob/master/README.md) to learn what OTS does and why it might be useful to you.

For details about configuring the [Ansible role for OTS](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3cspgyZXPNcnzNXCYKsEGJK7dKKA), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3cspgyZXPNcnzNXCYKsEGJK7dKKA/tree/docs/configuring-ots.md) online
- 📁 `roles/galaxy/ots/docs/configuring-ots.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ots                                                                  #
#                                                                      #
########################################################################

ots_enabled: true

ots_hostname: mash.example.com
ots_path_prefix: /ots

########################################################################
#                                                                      #
# /ots                                                                 #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the OTS instance becomes available at the URL specified with `ots_hostname`. With the configuration above, the service is hosted at `https://mash.example.com/ots`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3cspgyZXPNcnzNXCYKsEGJK7dKKA/tree/docs/configuring-ots.md#troubleshooting) on the role's documentation for details.
