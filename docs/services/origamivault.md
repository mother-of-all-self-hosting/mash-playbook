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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# OrigamiVault

The playbook can install and configure [OrigamiVault](https://github.com/origamivault/origamivault) for you.

OrigamiVault is a web application encrypting or splitting secrets for printing them as QR codes on sheets of paper for later recovery with JavaScript. The application can also work offline on a web browser.

See the project's [documentation](https://github.com/origamivault/origamivault/blob/main/README.md) to learn what OrigamiVault does and why it might be useful to you.

For details about configuring the [Ansible role for OrigamiVault](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3aGv2oUAxqmoGddtk1VwRioUTKbs), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3aGv2oUAxqmoGddtk1VwRioUTKbs/tree/docs/configuring-origamivault.md) online
- 📁 `roles/galaxy/origamivault/docs/configuring-origamivault.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# origamivault                                                         #
#                                                                      #
########################################################################

origamivault_enabled: true

origamivault_hostname: mash.example.com
origamivault_path_prefix: /origamivault

########################################################################
#                                                                      #
# /origamivault                                                        #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the OrigamiVault instance becomes available at the URL specified with `origamivault_hostname`. With the configuration above, the service is hosted at `https://mash.example.com/origamivault`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3aGv2oUAxqmoGddtk1VwRioUTKbs/tree/docs/configuring-origamivault.md#troubleshooting) on the role's documentation for details.
