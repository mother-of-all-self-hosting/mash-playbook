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

The playbook can install and configure [Fider](https://github.com/getfider/fider) for you.

Fider is a feedback portal for feature requests and suggestions.

See the project's [documentation](https://docs.fider.io/) to learn what Fider does and why it might be useful to you.

For details about configuring the [Ansible role for Fider](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3Fe49p3uVZpC43KdB5gDCTmr8u7Y), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3Fe49p3uVZpC43KdB5gDCTmr8u7Y/tree/docs/configuring-fider.md) online
- 📁 `roles/galaxy/fider/docs/configuring-fider.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [exim-relay](exim-relay.md) mailer — required on the default configuration; alternatively it is possible to use one of the SMTP servers which catch outgoing messages like [Mailpit](mailpit.md)

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

## Usage

After installation, the Fider instance becomes available at the URL specified with `fider_hostname`. With the configuration above, the service is hosted at `https://fider.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3Fe49p3uVZpC43KdB5gDCTmr8u7Y/tree/docs/configuring-fider.md#troubleshooting) on the role's documentation for details.
