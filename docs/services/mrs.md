# Matrix Rooms Search API

[Matrix Rooms Search](https://gitlab.com/etke.cc/mrs) is a fully-featured, standalone, matrix rooms search service.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mrs                                                                  #
#                                                                      #
########################################################################

mrs_enabled: true
mrs_hostname: mrs.example.com

mrs_admin_login: admin
mrs_admin_password: changeme
mrs_admin_ips:
	- 123.123.123.123

mrs_servers:
	- matrix.org

########################################################################
#                                                                      #
# /mrs                                                                 #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mrs.example.com`.


## Usage

After installation, call the `https://mrs.example.com/-/full` endpoint using admin credentials to discover and parse content

[API documentation](https://gitlab.com/etke.cc/mrs/api/-/blob/main/openapi.yml)
