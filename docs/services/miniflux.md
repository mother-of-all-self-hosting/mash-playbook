<!--
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Miniflux

[Miniflux](https://miniflux.app/) is a minimalist and opinionated feed reader.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# miniflux                                                             #
#                                                                      #
########################################################################

miniflux_enabled: true

miniflux_hostname: mash.example.com
miniflux_path_prefix: /miniflux

miniflux_admin_login: your-username-here
miniflux_admin_password: a-strong-password-here

########################################################################
#                                                                      #
# /miniflux                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Miniflux instance becomes available at the URL specified with `miniflux_hostname` and `miniflux_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/miniflux`.

To get started, open the URL with a web browser to log in. You can create additional users (admin-privileged or not) after logging in with your administrator login (`miniflux_admin_login`) and password (`miniflux_admin_password`).

## Related services

- [FreshRSS](freshrss.md) — Lightweight and powerful self-hosted RSS and Atom feed aggregator
- [ReactFlux](reactflux.md) — Third-party web frontend for Miniflux, aimed at providing a more user-friendly reading experience
