<!--
SPDX-FileCopyrightText: 2025 Gergely Horváth
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

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
labelstudio_hostname: labelstudio.example.com

########################################################################
#                                                                      #
# /LabelStudio                                                         #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `labelstudio.example.com`.

## Usage

After running the command for installation, the LabelStudio instance becomes available at the URL specified with `labelstudio_hostname`. With the configuration above, the service is hosted at `https://labelstudio.example.com`.

To get started, open the URL with a web browser to register new accounts, log in with them, and start working.

Keep in mind that every user will see every project.
It may be more secure to disable user registration and use an admin use (created during setup) to send out sign-up emails to additional users later on.

This admin user can be enabled by using the following settings:

```yml
labelstudio_environment_variables_disable_signup_without_link: true
labelstudio_environment_variables_username: "admin-username"
labelstudio_environment_variables_password: "admin-user-password"
```


## Recommended other services

It is possible to attach a pre-labeling backend to LabelStudio.
One such example project can be found in [this repository](https://github.com/seblful/label-studio-yolo-backend).
