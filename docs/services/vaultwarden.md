<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Vaultwarden

[Vaultwarden](https://github.com/dani-garcia/vaultwarden) (unofficial [Bitwarden](https://bitwarden.com/) compatible server) is a password manager server that you can use with the official **Bitwarden** apps and browser addons.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server
- (optional) the [exim-relay](exim-relay.md) mailer


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# vaultwarden                                                          #
#                                                                      #
########################################################################

vaultwarden_enabled: true

vaultwarden_hostname: mash.example.com

# For additional security, we recommend hosting Vaultwarden at a subpath.
# See: https://github.com/dani-garcia/vaultwarden/wiki/Hardening-Guide#hiding-under-a-subdir
#
# Choose your own custom path below.
# When using a path prefix, Vaultwarden will be available at: https://VAULTWARDEN_DOMAIN/PATH_PREFIX
# while the homepage (/) shows a 404 HTTP error.
#
# If you'd like to host at the root (without a path prefix), remove this configuration line.
vaultwarden_path_prefix: /vaultwarden-secret-custom-prefix

# Configure a strong admin secret here (generated with `pwgen -s 64 1`, etc).
# You will need this for accessing the /admin section useful for creating your first user
# and for doing various maintenance tasks.
# In the future, you can also consider disabling the /admin section by removing this configuration line.
vaultwarden_config_admin_token: ''

# Require people to validate their email addresses. When enabled, SMTP settings (below) are required.
vaultwarden_config_signups_verify: true

# Example SMTP settings.
# If you keep `vaultwarden_config_signups_verify` enabled, you will need to specify them.
# There are more SMTP variables in `roles/custom/devture_vaultwarden/defaults/main.yml`, in case you need them.
# If you decide you won't set up SMTP, consider removing all these configuration lines below
# and removing `vaultwarden_config_signups_verify: true` above.
vaultwarden_config_smtp_from: vaultwarden@DOMAIN
vaultwarden_config_smtp_host: ''
vaultwarden_config_smtp_port: 587
vaultwarden_config_smtp_security: starttls
vaultwarden_config_smtp_username: ''
vaultwarden_config_smtp_password: ''

########################################################################
#                                                                      #
# /vaultwarden                                                         #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Vaultwarden instance becomes available at the URL specified with `vaultwarden_hostname` and `vaultwarden_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/vaultwarden-secret-custom-prefix`.

To get started, open the URL `https://mash.example.com/vaultwarden-secret-custom-prefix/admin` with a web browser, and create a first user account. Note the URL is accessible with an admin token, as specified with `vaultwarden_config_admin_token` on your `vars.yml` file.

If you hadn't enabled the `/admin` feature (by defining `vaultwarden_config_admin_token`), you would:

- **either** need to do so and [re-run the playbook](../installing.md) (you can do it quickly with `just install-service vaultwarden`)
- **or** to enable public registration (`vaultwarden_config_signups_enabled: true`) at least temporarily.
