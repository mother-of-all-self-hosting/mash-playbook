<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Radicale

[Radicale](https://radicale.org/) is a Free and Open-Source CalDAV and CardDAV Server (solution for hosting contacts and calendars).


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

radicale_credentials:
  - username: someone
    password: secret-password
  - username: another
    password: more-secret-password

########################################################################
#                                                                      #
# /radicale                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Radicale instance becomes available at the URL specified with `radicale_hostname` and `radicale_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/radicale`.

You can log in with your credentials (see the `radicale_credentials` configuration variable).

Creating new users requires changing the `radicale_credentials` variable and [re-running the playbook](../installing.md). You can rebuild only this service quickly by running: `just install-service radicale`.
