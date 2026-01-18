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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Moner.ooo

The playbook can install and configure [Moner.ooo](https://github.com/nice42q/moner.ooo) for you.

Moner.ooo is a service for checking Monero / fiat exchange rates in various currencies.

See the project's [documentation](https://github.com/nice42q/moner.ooo/blob/main/README.md) to learn what Moner.ooo does and why it might be useful to you.

For details about configuring the [Ansible role for Moner.ooo](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3i2ogEXxuSzVAxVaRuoydAiDCBKi), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3i2ogEXxuSzVAxVaRuoydAiDCBKi/tree/docs/configuring-monerooo.md) online
- 📁 `roles/galaxy/monerooo/docs/configuring-monerooo.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# moner.ooo                                                            #
#                                                                      #
########################################################################

monerooo_enabled: true

monerooo_hostname: monerooo.example.com

########################################################################
#                                                                      #
# /moner.ooo                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting Moner.ooo under a subpath (by configuring the `monerooo_path_prefix` variable) does not seem to be possible due to Moner.ooo's technical limitations.

## Usage

After running the command for installation, the Moner.ooo instance becomes available at the URL specified with `monerooo_hostname`. With the configuration above, the service is hosted at `https://monerooo.example.com`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3i2ogEXxuSzVAxVaRuoydAiDCBKi/tree/docs/configuring-monerooo.md#troubleshooting) on the role's documentation for details.
