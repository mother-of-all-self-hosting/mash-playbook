<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Fider

The playbook can install and configure [Fider](https://github.com/asciinema/fider/) for you.

Fider is a server-side component of the asciinema system, a suite of tools for recording, streaming, and sharing terminal sessions. The [asciinema CLI](https://docs.asciinema.org/manual/cli/) can be configured to upload recordings to the server this role sets up, so that users can host and share them on it, instead of the default Fider (<https://asciinema.org>).

See the project's [documentation](https://docs.asciinema.org/) to learn what asciinema does and why it might be useful to you.

For details about configuring the [Ansible role for Fider](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzcSq6tnVLBUQ88zSRLThc7A7RDZb), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzcSq6tnVLBUQ88zSRLThc7A7RDZb/tree/docs/configuring-fider.md) online
- 📁 `roles/galaxy/fider/docs/configuring-fider.md` locally, if you have [fetched the Ansible roles](../installing.md)

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
# fider                                                                #
#                                                                      #
########################################################################

fider_enabled: true

fider_hostname: fider.example.com

########################################################################
#                                                                      #
# /fider                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting Fider under a subpath (by configuring the `fider_path_prefix` variable) does not seem to be possible due to Fider's technical limitations.

### Set a random string for secret key base

You also need to set a random string used for cryptographic operations, such as signing and verification of session cookies. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
fider_environment_variable_secret_key_base: YOUR_SECRET_KEY_HERE
```

### Configure the mailer

You can configure a SMTP mailer for functions such as sending links for logging in. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

If you do not want to enable a mailer for Fider altogether, add the following configuration to your `vars.yml` file:

```yaml
fider_mailer_enabled: false
```

>[!NOTE]
> If a SMTP server is not configured, you'll need to obtain such a link from the server container logs *every time* to log in.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
fider_environment_variable_sign_up_disabled: false
```

### Requiring authentication on uploading

By default uploading recordings with `asciinema upload` requires authentication with `asciinema auth`. To disable it and allow anyone to upload them, add the following configuration to your `vars.yml` file:

```yaml
fider_environment_variable_upload_auth_required: false
```

## Usage

After installation, the Fider instance becomes available at the URL specified with `fider_hostname`. With the configuration above, the service is hosted at `https://fider.example.com`.

To get started, install the asciinema CLI on your local computer, and then point it to the server, so that the CLI will upload your recordings to it. The basic flow to use the CLI from recording a terminal session to upload the recording to your server is available on [this page](https://docs.asciinema.org/getting-started/).

Since account registration is disabled by default, you might want to enable it first by setting `fider_environment_variable_sign_up_disabled` to `false` temporarily in order to create your own account.

Adding an authentication proxy service like [Keycloak](keycloak.md) and [Tinyauth](tinyauth.md) in front of the Fider to limit who can access to its web interface is also worth considering.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzcSq6tnVLBUQ88zSRLThc7A7RDZb/tree/docs/configuring-fider.md#troubleshooting) on the role's documentation for details.
