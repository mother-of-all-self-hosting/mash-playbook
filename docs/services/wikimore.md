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

# Wikimore

The playbook can install and configure [Wikimore](https://git.private.coffee/PrivateCoffee/wikimore/) for you.

Wikimore allows you to browse Wikipedia projects without exposing your IP address, browsing habits, and other browser fingerprinting data to them.

See the project's [documentation](https://git.private.coffee/PrivateCoffee/wikimore/src/branch/main/README.md) to learn what Wikimore does and why it might be useful to you.

For details about configuring the [Ansible role for Wikimore](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az54oV5qKRrLSArZqdisrD9s7h9BQ), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az54oV5qKRrLSArZqdisrD9s7h9BQ/tree/docs/configuring-wikimore.md) online
- 📁 `roles/galaxy/wikimore/docs/configuring-wikimore.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# wikimore                                                             #
#                                                                      #
########################################################################

wikimore_enabled: true

wikimore_hostname: wikimore.example.com

########################################################################
#                                                                      #
# /wikimore                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Wikimore under a subpath (by configuring the `wikimore_path_prefix` variable) does not seem to be possible due to Wikimore's technical limitations.

## Usage

After running the command for installation, the Wikimore instance becomes available at the URL specified with `wikimore_hostname`. With the configuration above, the service is hosted at `https://wikimore.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to Wikimore.

If you would like to publish your instance so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://git.private.coffee/PrivateCoffee/wikimore/) to add yours to [`instances.json`](https://git.private.coffee/PrivateCoffee/wikimore/src/branch/main/instances.json), which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)).

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az54oV5qKRrLSArZqdisrD9s7h9BQ/tree/docs/configuring-wikimore.md#troubleshooting) on the role's documentation for details.

## Related services

- [AnonymousOverflow](anonymousoverflow.md) — Frontend for StackOverflow
- [Mozhi](mozhi.md) — Frontend for translation engines
- [Redlib](redlib.md) — Frontend for Reddit
