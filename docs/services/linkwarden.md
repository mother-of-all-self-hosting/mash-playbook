<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Linkwarden

The playbook can install and configure [Linkwarden](https://github.com/linkwarden/linkwarden/) for you.

Linkwarden is a server-side component of the linkwarden system, a suite of tools for recording, streaming, and sharing terminal sessions. The [linkwarden CLI](https://docs.linkwarden.org/manual/cli/) can be configured to upload recordings to the server this role sets up, so that users can host and share them on it, instead of the default Linkwarden (<https://linkwarden.org>).

See the project's [documentation](https://docs.linkwarden.org/) to learn what linkwarden does and why it might be useful to you.

For details about configuring the [Ansible role for Linkwarden](https://codeberg.org/acioustick/ansible-role-linkwarden), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-linkwarden/src/branch/master/docs/configuring-linkwarden.md) online
- 📁 `roles/galaxy/linkwarden/docs/configuring-linkwarden.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer — required on the default configuration

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# linkwarden                                                           #
#                                                                      #
########################################################################

linkwarden_enabled: true

linkwarden_hostname: linkwarden.example.com

########################################################################
#                                                                      #
# /linkwarden                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting Linkwarden under a subpath (by configuring the `linkwarden_path_prefix` variable) does not seem to be possible due to Linkwarden's technical limitations.

### Set a random string for secret key base

You also need to set a random string used for cryptographic operations, such as signing and verification of session cookies. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
linkwarden_environment_variable_secret_key_base: YOUR_SECRET_KEY_HERE
```

### Configure the mailer

You can configure a SMTP mailer for functions such as sending links for logging in. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

If you do not want to enable a mailer for Linkwarden altogether, add the following configuration to your `vars.yml` file:

```yaml
linkwarden_mailer_enabled: false
```

>[!NOTE]
> If a SMTP server is not configured, you'll need to obtain such a link from the server container logs *every time* to log in.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
linkwarden_environment_variable_sign_up_disabled: false
```

### Requiring authentication on uploading

By default uploading recordings with `linkwarden upload` requires authentication with `linkwarden auth`. To disable it and allow anyone to upload them, add the following configuration to your `vars.yml` file:

```yaml
linkwarden_environment_variable_upload_auth_required: false
```

## Usage

After installation, the Linkwarden instance becomes available at the URL specified with `linkwarden_hostname`. With the configuration above, the service is hosted at `https://linkwarden.example.com`.

To get started, install the linkwarden CLI on your local computer, and then point it to the server, so that the CLI will upload your recordings to it. The basic flow to use the CLI from recording a terminal session to upload the recording to your server is available on [this page](https://docs.linkwarden.org/getting-started/).

Since account registration is disabled by default, you might want to enable it first by setting `linkwarden_environment_variable_sign_up_disabled` to `false` temporarily in order to create your own account.

Adding an authentication proxy service like [Keycloak](keycloak.md) and [Tinyauth](tinyauth.md) in front of the Linkwarden to limit who can access to its web interface is also worth considering.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-linkwarden/src/branch/master/docs/configuring-linkwarden.md#troubleshooting) on the role's documentation for details.
