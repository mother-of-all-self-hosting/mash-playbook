# EchoIP

[EchoIP](https://github.com/mpolden/echoip) is simple service for looking up your IP address, powering [ifconfig.co](https://ifconfig.co)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# echoip                                                               #
#                                                                      #
########################################################################

echoip_enabled: true

echoip_hostname: echoip.example.com

########################################################################
#                                                                      #
# /echoip                                                              #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://echoip.example.com`.


## Usage

```bash
curl https://echoip.example.com
```
