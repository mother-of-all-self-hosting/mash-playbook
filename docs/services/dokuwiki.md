# DokuWiki

[DokuWiki](https://dokuwiki.org/) is a lightweight, file-based wiki engine with intuitive syntax and no database requirements.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# dokuwiki                                                             #
#                                                                      #
########################################################################

dokuwiki_enabled: true

dokuwiki_hostname: dokuwiki.example.com

########################################################################
#                                                                      #
# /dokuwiki                                                            #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://dokuwiki.example.com/`.

## Usage

You will have to open the URL `https://dokuwiki.example.com/install.php` to complete the setup, as described in the official [setup instructions](https://www.dokuwiki.org/installer).
