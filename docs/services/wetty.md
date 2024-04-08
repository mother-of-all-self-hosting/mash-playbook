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

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/wetty` and connect to `example.com` on port `22`.

You can remove the `wetty_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

## Usage

After installation, you should be able to access your new Wetty instance at: `https://WETTY_DOMAIN/PATH_PREFIX`, where:

- `WETTY_DOMAIN` matches your domain, as specified in `wetty_hostname` in your `vars.yml` file
- `PATH_PREFIX` matches your path prefix, as specified in `wetty_path_prefix` in your `vars.yml` file

Once connected, simply input the username and password to use. Keep in mind that Wetty only supports password authentication, so if the SSH daemon at `wetty_ssh_host` only allows pubkey authentication you will not be able to connect.
