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

# Tinyauth

The playbook can install and configure [Tinyauth](https://github.com/httpjamesm/Tinyauth) for you.

Tinyauth allows you to view StackOverflow threads without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://github.com/httpjamesm/Tinyauth/blob/main/README.md) to learn what Tinyauth does and why it might be useful to you.

For details about configuring the [Ansible role for Tinyauth](https://github.com/mother-of-all-self-hosting/ansible-role-tinyauth), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-tinyauth/blob/main/docs/configuring-tinyauth.md) online
- 📁 `roles/galaxy/tinyauth/docs/configuring-tinyauth.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# tinyauth                                                             #
#                                                                      #
########################################################################

tinyauth_enabled: true

tinyauth_hostname: tinyauth.example.com

########################################################################
#                                                                      #
# /tinyauth                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Tinyauth under a subpath (by configuring the `tinyauth_path_prefix` variable) does not seem to be possible due to Tinyauth's technical limitations.

## Usage

After running the command for installation, Tinyauth becomes available at the specified hostname like `https://tinyauth.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to Tinyauth. See [this section](https://github.com/httpjamesm/Tinyauth/blob/main/README.md#how-to-make-stack-overflow-links-take-you-to-tinyauth-automatically) on the official documentation for more information.

If you would like to publish your instance so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://github.com/httpjamesm/Tinyauth) to add yours to [`instances.json`](https://github.com/httpjamesm/Tinyauth/blob/main/instances.json), which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tinyauth/blob/main/docs/configuring-tinyauth.md#troubleshooting) on the role's documentation for details.

## Related services

- [Authelia](authelia.md) — Open-source authentication and authorization server that can work as a companion to common reverse proxies like Traefik
- [authentik](authentik.md) — Open-source identity provider focused on flexibility and versatility
- [Keycloak](keycloak.md) — Open source identity and access management solution
