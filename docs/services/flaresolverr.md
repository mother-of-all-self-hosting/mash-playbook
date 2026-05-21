<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 sudo-Tiz
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FlareSolverr

The playbook can install and configure [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) for you.

FlareSolverr is an open-source proxy server to bypass Cloudflare protection.

See the project's [documentation](https://github.com/FlareSolverr/FlareSolverr/blob/master/README.md) to learn what FlareSolverr does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

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

## Usage

After running the command for installation, the FlareSolverr instance becomes available and starts running on the server, listening to the specified port (port 8191 by default) and is reachable from other services.

If you need the container to be accessible from outside, you can use `flaresolverr_container_http_bind_port` or `flaresolverr_hostname`.

> **Note:**
> The `flaresolverr_path_prefix` variable can be adjusted to host under a subpath (e.g., `flaresolverr_path_prefix: /flaresolverr`), but this configuration has not been tested yet.

For additional configuration options, refer to the [ansible-role-flaresolverr](https://github.com/sudo-Tiz/ansible-role-flaresolverr)'s `defaults/main.yml` file.
