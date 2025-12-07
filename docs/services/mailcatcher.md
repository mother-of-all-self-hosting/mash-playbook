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

# MailCatcher

The playbook can install and configure [MailCatcher](https://codeberg.org/mailcatcher/mailcatcher) for you.

MailCatcher allows you to view GitHub repositories without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://codeberg.org/mailcatcher/mailcatcher/src/branch/dev/README.md) to learn what MailCatcher does and why it might be useful to you.

For details about configuring the [Ansible role for MailCatcher](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzFVv3koKtheJTTwPSjF3J6DajePK), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzFVv3koKtheJTTwPSjF3J6DajePK/tree/docs/configuring-mailcatcher.md) online
- 📁 `roles/galaxy/mailcatcher/docs/configuring-mailcatcher.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mailcatcher                                                          #
#                                                                      #
########################################################################

mailcatcher_enabled: true

mailcatcher_hostname: mailcatcher.example.com

########################################################################
#                                                                      #
# /mailcatcher                                                         #
#                                                                      #
########################################################################
```

**Note**: hosting MailCatcher under a subpath (by configuring the `mailcatcher_path_prefix` variable) does not seem to be possible due to MailCatcher's technical limitations.

There are other settings which need configuring such as ones about instance's management and its transparency. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzFVv3koKtheJTTwPSjF3J6DajePK/tree/docs/configuring-mailcatcher.md#enable-disable-proxying-non-essential-data) on the role's documentation for details.

## Usage

After running the command for installation, the MailCatcher instance becomes available at the URL specified with `mailcatcher_hostname`. With the configuration above, the service is hosted at `https://mailcatcher.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to MailCatcher.

If you would like to make your instance public so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://codeberg.org/mailcatcher/mailcatcher-instances) to add yours to [`instances.json`](https://codeberg.org/mailcatcher/mailcatcher-instances/src/branch/master/instances.json), which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)).

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzFVv3koKtheJTTwPSjF3J6DajePK/tree/docs/configuring-mailcatcher.md#troubleshooting) on the role's documentation for details.

## Related services

- [Mozhi](mozhi.md) — Frontend for translation engines
- [Redlib](redlib.md) — Frontend for Reddit
