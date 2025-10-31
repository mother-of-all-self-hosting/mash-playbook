<!--
SPDX-FileCopyrightText: 2025 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Headplane

[Headplane](https://headplane.net/) is an open source, self-hosted implementation of the [Tailscale Web UI](https://tailscale.com/) for [Headscale](headscale.md).

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- a [Headscale](headscale.md) server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# headplane                                                            #
#                                                                      #
########################################################################

headplane_enabled: true

headplane_hostname: headplane.example.com

########################################################################
#                                                                      #
# /headplane                                                           #
#                                                                      #
########################################################################
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- The [Headplane role](https://github.com/spatterIight/ansible-role-headplane/)'s [`defaults/main.yml`](https://github.com/spatterIight/ansible-role-headplane/blob/main/defaults/main.yml) for additional variables that you can customize via your `vars.yml` file.

## Usage

After running the command for installation, the Headplane instance becomes available at the URL specified with `headplane_hostname`. With the configuration above, the service is hosted at `https://headplane.example.com/admin`.

The application being hosted at `/admin` is [not easily configurable](https://github.com/tale/headplane/blob/main/docs/install/native-mode.md#custom-path-prefix). The default configuration is to automatically redirect `/` requests to `/admin`.

> [!NOTE]
> The `headplane_path_prefix` variable can be adjusted to host under a subpath (e.g. `headplane_path_prefix: /headplane`), but this hasn't been tested yet.

### Logging in

To [access headplane](https://headplane.net/install/docker#accessing-headplane), run a command using the [Headscale convenience script](headscale.md#convenience-script-to-call-the-binary) like this:

```sh
/mash/headscale/bin/headscale apikeys create
```

Then login to `https://headplane.example.com/admin` by entering the generated API key.
