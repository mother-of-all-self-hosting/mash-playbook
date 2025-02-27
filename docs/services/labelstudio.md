# LabelStudio

[LabelStudio](https://labelstud.io/) is an open source data labeling tool that supports multiple projects.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# LabelStudio                                                          #
#                                                                      #
########################################################################

labelstudio_enabled: true
labelstudio_hostname: "example.labelstudio.hostname.com"

########################################################################
#                                                                      #
# /LabelStudio                                                         #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `example.labelstudio.hostname.com`.
Also, PostgreSQL backend is used based on [the official documentation](https://labelstud.io/guide/storedata#PostgreSQL-database).

## Usage

After installation, you should be able to access your new LabelStudio instance at the configured URL (see above).

Going there, you can register new accounts, login with them and start working.
Keep in mind that every user will see every project.
It may be more secure to disable user registration and use an admin user---created during setup---to send out sign-up emails for wannabe users.
This admin user can be enabled by the following settings:

```yml
labelstudio_environment_variables_disable_signup_without_link: true
labelstudio_environment_variables_username: "admin-username"
labelstudio_environment_variables_password: "admin-user-password"
```


## Recommended other services

It is possible to attach a pre-labeling backend to LabelStudio.
One such example project can be found in [this repository](https://github.com/seblful/label-studio-yolo-backend).
Although we created a role for such backends in-house, currently it is not in a state to be upstreamed as it contains too many specific variables.
