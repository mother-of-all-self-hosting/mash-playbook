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
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FlareSolverr

The playbook can install and configure [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) for you.

FlareSolverr is an open-source proxy server to bypass Cloudflare protection.

See the project's [documentation](https://github.com/FlareSolverr/FlareSolverr/blob/master/README.md) to learn what FlareSolverr does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — Reverse-proxy server for exposing FlareSolverr publicly

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# flaresolverr                                                         #
#                                                                      #
########################################################################

flaresolverr_enabled: true

########################################################################
#                                                                      #
# /flaresolverr                                                        #
#                                                                      #
########################################################################
```

### Expose the instance publicly (optional)

By default, the FlareSolverr instance is not exposed externally, as it is mainly intended to be used in the internal network.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which FlareSolverr is served.
flaresolverr_hostname: "flaresolverr.example.com"
```

## Usage

After running the command for installation, FlareSolverr becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the URL specified with `flaresolverr_hostname`. With the configuration above, the service is hosted at `https://flaresolverr.example.com`.
