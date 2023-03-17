# Redmine

[Redmine](https://redmine.org/) is a flexible project management web application. Written using the Ruby on Rails framework, it is cross-platform and cross-database.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# redmine                                                             #
#                                                                      #
########################################################################

redmine_enabled: true

redmine_hostname: redmine.example.com

########################################################################
#                                                                      #
# /redmine                                                            #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://redmine.example.com`.


## Usage

After installation, you can register your administrator account

You can create additional users (admin-privileged or not) after that.
