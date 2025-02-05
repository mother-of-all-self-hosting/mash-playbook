# Sonarr

[Sonarr](https://sonarr.tv/) is a smart PVR for newsgroup and bittorrent users.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# sonarr                                                               #
#                                                                      #
########################################################################

sonarr_enabled: true

sonarr_hostname: sonarr.example.com

########################################################################
#                                                                      #
# /sonarr                                                              #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://sonarr.example.com`.

A `sonarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `sonarr_path_prefix: /sonarr`), but this hasn't been tested yet.

## Usage

After [installation](../installing.md), you should be able to access your new Sonarr instance at the URL you've chosen.

For additional configuration options, refer to [ansible-role-sonarr](https://github.com/spatterIight/ansible-role-sonarr)'s `defaults/main.yml` file.
