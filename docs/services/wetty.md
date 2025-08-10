<!--
SPDX-FileCopyrightText: 2023 - 2025 MASH project contributors
SPDX-FileCopyrightText: 2023 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Wetty

[Wetty](https://github.com/butlerx/wetty/tree/main) is an SSH terminal over HTTP/HTTPS, useful for when on a strict network which disallows outbound SSH traffic, or when only a browser can be used (like a managed chromebook).

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# wetty                                                                #
#                                                                      #
########################################################################

wetty_enabled: true
wetty_hostname: mash.example.com
wetty_path_prefix: /wetty
wetty_ssh_host: example.com
wetty_ssh_port: 22

########################################################################
#                                                                      #
# /wetty                                                               #
#                                                                      #
########################################################################
```

### Configure SSH port for Wetty (optional)

Wetty uses port 22 for its SSH feature by default.

If you wish to have the instance listen to another port, add the following configuration to your `vars.yml` file and adjust the port as you see fit.

```yaml
wetty_ssh_port: 222
```

## Usage

After running the command for installation, the Wetty instance becomes available at the URL specified with `wetty_hostname` and `wetty_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/wetty` and connects to `example.com` on port `22`.

Once connected, you can log in with SSH with the username and password.

>[!NOTE]
> Wetty only supports password authentication, so if the SSH daemon at `wetty_ssh_host` only allows pubkey authentication you will not be able to connect.
