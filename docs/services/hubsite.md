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
SPDX-FileCopyrightText: 2023 - 2025 MASH project contributors
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Hubsite

The playbook can install and configure [Hubsite](https://github.com/moan0s/hubsite) for you.

Hubsite is a simple, static site that shows an overview of available services. It makes use of the official nginx docker image.

See the project's [documentation](https://github.com/moan0s/hubsite/blob/main/README.md) to learn what Hubsite does and why it might be useful to you.

For details about configuring the [Ansible role for Hubsite](https://github.com/mother-of-all-self-hosting/ansible-role-hubsite), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-hubsite/blob/main/docs/configuring-hubsite.md) online
- 📁 `roles/galaxy/hubsite/docs/configuring-hubsite.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# hubsite                                                              #
#                                                                      #
########################################################################

hubsite_enabled: true

hubsite_hostname: hubsite.example.com

########################################################################
#                                                                      #
# /hubsite                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting Hubsite under a subpath (by configuring the `hubsite_path_prefix` variable) does not seem to be possible due to Hubsite's technical limitations.

### Specify headers on the UI

You also need to specify headers on the UI by adding configurations to your `vars.yml` file. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-hubsite/blob/main/docs/configuring-hubsite.md#specify-headers-on-the-ui) on the role's documentation for details.

## Usage

After running the command for installation, the Hubsite instance becomes available at the URL specified with `hubsite_hostname`. With the configuration above, the service is hosted at `https://hubsite.example.com`.

>[!NOTE]
> You can SSO-protect this website with the help of [Authelia](authelia.md) or [OAuth2-Proxy](oauth2-proxy.md) (connected to any OIDC provider).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-hubsite/blob/main/docs/configuring-hubsite.md#troubleshooting) on the role's documentation for details.

You can alternatively output the page manually. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-hubsite/blob/main/docs/configuring-hubsite.md#usage) on the role's documentation for details.

## Related services

- [Homarr](homarr.md) — customizable dashboard for managing your favorite applications and services
