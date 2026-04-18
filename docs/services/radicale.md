<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Radicale

The playbook can install and configure [Radicale](https://radicale.org/) for you.

Radicale is a Free and Open-Source CalDAV and CardDAV Server (solution for hosting contacts and calendars).

See the project's [documentation](https://radicale.org/v3.html#documentation-1) to learn what Radicale does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# radicale                                                             #
#                                                                      #
########################################################################

radicale_enabled: true

radicale_hostname: mash.example.com
radicale_path_prefix: /radicale

# Generate each entry with `htpasswd -nb USERNAME PASSWORD`
# and paste the whole `USERNAME:HASH` line below.
# Example:
# htpasswd -nb someone 'secret-password'
# htpasswd -nb another 'more-secret-password'
radicale_htpasswds:
  - 'someone:$apr1$Dz1QzvR9$TQj8rP2QfLz7dYkP6Y0K4/'
  - 'another:$apr1$QfJ1mU7a$gR0d9D0dKfIDm0w3lN4hY0'

########################################################################
#                                                                      #
# /radicale                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Radicale instance becomes available at the URL specified with `radicale_hostname` and `radicale_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/radicale`.

You can log in with your credentials (see the `radicale_htpasswds` configuration variable).

Generate entries outside Ansible with `htpasswd -nb USERNAME PASSWORD` and put the resulting lines into `radicale_htpasswds`.

The legacy `radicale_credentials` convenience variable is discouraged, because it depends on the `passlib` Python library, may be affected by passlib/bcrypt compatibility issues (see: https://foss.heptapod.net/python-libs/passlib/-/issues/196), and produces non-deterministic hashes which can trigger unnecessary Ansible changes.

Creating new users requires changing the `radicale_htpasswds` variable and [re-running the playbook](../installing.md). You can rebuild only this service quickly by running: `just install-service radicale`.
