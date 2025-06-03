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

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/miniflux`.

You can remove the `miniflux_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.


## Usage

After installation, you can log in with your administrator login (`miniflux_admin_login`) and password (`miniflux_admin_password`).

You can create additional users (admin-privileged or not) after logging in.

## Related services

- [ReactFlux](reactflux.md) — Third-party web frontend for Miniflux, aimed at providing a more user-friendly reading experience
