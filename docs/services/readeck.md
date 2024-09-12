# Readeck

[Readeck](https://readeck.org) is a simple web application that lets you save the precious readable content of web pages you like and want to keep forever.
See it as a bookmark manager and a read later tool.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# Readeck                                                              #
#                                                                      #
########################################################################

readeck_enabled: true

readeck_hostname: readeck.example.com

########################################################################
#                                                                      #
# /Readeck                                                             #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://readeck.example.com/`.

## Usage

After installation, you can go to the Readeck URL, as defined in `readeck_hostname`, and create a user. The User Documentation is embedded in Readeck so it's easy to access and always up-to-date.
