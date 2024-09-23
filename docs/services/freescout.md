# Freescout

[Freescout](https://freescout.net/) is a free open-source helpdesk and shared inbox solution.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# freescout                                                            #
#                                                                      #
########################################################################

freescout_enabled: true

freescout_hostname: freescout.example.com

freescout_admin_email: your-email-here
freescout_admin_password: a-strong-password-here

########################################################################
#                                                                      #
# /freescout                                                           #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://freescout.example.com`.


## Usage

After installation, you can log in with your administrator login (`freescout_admin_email`) and password (`freescout_admin_password`).
