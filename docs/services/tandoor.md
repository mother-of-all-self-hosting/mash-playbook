# Tandoor

[Tandoor](https://docs.tandoor.dev/) is a recipe manager that allows you to manage your ever growing collection of digital recipes.


## Dependencies

This service requires the following other services:
- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# tandoor                                                            #
#                                                                      #
########################################################################

tandoor_enabled: true

tandoor_hostname: tandoor.example.com
#path prefix is not supported at the moment
#tandoor_path_prefix: /tandoor



########################################################################
#                                                                      #
# /tandoor                                                           #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://tandoor.example.com/`.

### Authentication

On first use (see [Usage](#usage) below), you'll be asked to create the first administrator user.

You can create additional users from the web UI after that.


## Usage

After installation, you can go to the Tandoor URL, as defined in `tandoor_hostname` and `tandoor_path_prefix`.

As mentioned in [Authentication](#authentication) above, you'll be asked to create the first administrator user the first time you open the web UI.
