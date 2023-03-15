# Uptime-kuma

[Uptime-kuma](https://uptime.kuma.pet/) is a fancy self-hosted monitoring tool.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# uptime-kuma                                                          #
#                                                                      #
########################################################################

uptime_kuma_enabled: true

uptime_kuma_hostname: mash.example.com

# For now, hosting uptime-kuma under a path is not supported.
# See: https://github.com/louislam/uptime-kuma/issues/147
# uptime_kuma_path_prefix: /uptime-kuma

########################################################################
#                                                                      #
# /uptime-kuma                                                         #
#                                                                      #
########################################################################
```

## Usage

The first time you open the Uptime-kuma Web UI it will make you go through a setup wizard, which will set up your admin credentials.
