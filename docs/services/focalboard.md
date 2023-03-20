# Focalboard

[Focalboard](https://www.focalboard.com/) is an open source, self-hosted alternative to [Trello](https://trello.com/), [Notion](https://www.notion.so/), and [Asana](https://asana.com/)


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# focalboard                                                           #
#                                                                      #
########################################################################

focalboard_enabled: true

focalboard_hostname: mash.example.com
focalboard_path_prefix: /focalboard

########################################################################
#                                                                      #
# /focalboard                                                          #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/focalboard`.

You can remove the `focalboard_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.


## Usage

After [installation](../installing.md), you can go to the Focalboard URL you've configured above.

You can use the signup page to register the first (administrator) user. The first signup is always allowed. Users after the first one need an invitation link to sign up.
