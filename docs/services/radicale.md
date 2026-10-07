<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Radicale

The playbook can install and configure [Radicale](https://radicale.org/) for you.

Radicale is a free and open-source CalDAV and CardDAV server (solution for hosting contacts and calendars).

See the project's [documentation](https://radicale.org/v3.html#documentation-1) to learn what Radicale does and why it might be useful to you.

For details about configuring the [Ansible role for Radicale](https://github.com/mother-of-all-self-hosting/ansible-role-radicale), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-radicale/blob/main/docs/configuring-radicale.md) online
- 📁 `roles/galaxy/radicale/docs/configuring-radicale.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

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

########################################################################
#                                                                      #
# /radicale                                                            #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

For Radicale, it is configured to enable the HTTP Basic authentication by default. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-radicale/blob/main/docs/configuring-radicale.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up.

## Usage

After running the command for installation, the Radicale instance becomes available at the URL specified with `radicale_hostname` and `radicale_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/radicale`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-radicale/blob/main/docs/configuring-radicale.md#usage) on the role's documentation for details about usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-radicale/blob/main/docs/configuring-radicale.md#troubleshooting) on the role's documentation for details.
