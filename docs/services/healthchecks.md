# Healthchecks

[Healthchecks](https://healthchecks.io/) is simple and Effective **Cron Job Monitoring** solution.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# healthchecks                                                         #
#                                                                      #
########################################################################

healthchecks_enabled: true

healthchecks_hostname: mash.example.com
# Note: hosting under a path prefix is somewhat problematic. See below.
healthchecks_path_prefix: /healthchecks

########################################################################
#                                                                      #
# /healthchecks                                                        #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/healthchecks`.

You can remove the `healthchecks_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

**Note**: there are minor quirks when hosting under a subpath, such as:

- [Fonts not loading, because it attempts to load them from `/static` instead of `/path-prefix/static`](https://github.com/healthchecks/healthchecks/issues/822)

### Authentication

The first superuser account is created after installation. See [Usage](#usage).
You can create as many accounts as you wish.

### Email integration

To allow Healthchecks to send emails, add the following **additional** configuration:

```yaml
healthchecks_environment_variables_additional_variables: |
  DEFAULT_FROM_EMAIL=healthchecks@example.com
  EMAIL_HOST=smtp.example.com
  EMAIL_HOST_PASSWORD=
  EMAIL_HOST_USER=
  EMAIL_PORT=587
  EMAIL_USE_TLS=True
  EMAIL_USE_VERIFICATION=True
```

### Integrating with other services

Refer to the [upstream `.env.example` file](https://github.com/healthchecks/healthchecks/blob/master/docker/.env.example) for discovering additional environment variables.

You can pass these to the Healthchecks container using the `healthchecks_environment_variables_additional_variables` variable. See [Email integration](#email-integration) for an example.


## Usage

After installation, you need to **create a superuser account**.
This is an interactive process which can be initiated by **SSH-ing into into the server** and **running a command** like this:

```sh
docker exec -it mash-healthchecks /opt/healthchecks/manage.py createsuperuser
```

After creating the superuser account, you can go to the [Healthchecks URL](#url) to log in and start setting up healthchecks.


## Recommended other services

- [Prometheus](prometheus.md) - a metrics collection and alerting monitoring solution
