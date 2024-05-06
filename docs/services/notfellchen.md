# ILMO

[Notfellchen](https://codeberg.org/moanos/notfellchen) is a self-hosted tool to list animals available for adoption to increase their chance of finding a forever-home.


**Warning**: This service is a custom solution. Feel free to use it but don't expect a solution that works for every use case. Issues with this should be filed in the [project itself](https://codeberg.org/moanos/notfellchen).

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# notfellchen                                                          #
#                                                                      #
########################################################################

notfellchen_enabled: true
notfellchen_hostname: notfellchen.example.com

########################################################################
#                                                                      #
# /notfellchen                                                         #
#                                                                      #
########################################################################
```

## Setting up the first user

You need to create a first user (unless you import an existing database).
You can do this conveniently by running

```bash
just run-tags notfellchen-add-superuser --extra-vars=username=USERNAME --extra-vars=password=PASSWORD --extra-vars=email=EMAIL
```

## Usage

After installation, you can go to the URL, as defined in `notfellchen_hostname`. Log in with the user credentials from above.
