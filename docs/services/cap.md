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

# Cap Standalone

The playbook can install and configure [Cap Standalone](https://capjs.js.org/guide/standalone/) for you.

Cap Standalone is a self-hosted version of Cap's backend.

See the project's [documentation](https://capjs.js.org/guide/standalone/) to learn what Cap Standalone does and why it might be useful to you.

For details about configuring the [Ansible role for Cap Standalone](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSj65STd1FuR22pm4vLCSmFQ1rt5), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSj65STd1FuR22pm4vLCSmFQ1rt5/tree/docs/configuring-cap.md) online
- 📁 `roles/galaxy/cap/docs/configuring-cap.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# cap                                                                  #
#                                                                      #
########################################################################

cap_enabled: true

cap_hostname: cap.example.com

########################################################################
#                                                                      #
# /cap                                                                 #
#                                                                      #
########################################################################
```

**Note**: hosting Cap Standalone under a subpath (by configuring the `cap_path_prefix` variable) does not seem to be possible due to Cap Standalone's technical limitations.

### Set a password for the admin dashboard

You also need to set a password for the admin dashboard by adding the following configuration to your `vars.yml` file:

```yaml
cap_environment_variables_admin_key: YOUR_ADMIN_PASSWORD_HERE
```

Replace `YOUR_ADMIN_PASSWORD_HERE` with your own value.

## Usage

After running the command for installation, the Cap Standalone instance becomes available at the URL specified with `cap_hostname`. With the configuration above, the service is hosted at `https://cap.example.com`.

Refer to <https://capjs.js.org/guide/> for the usage.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSj65STd1FuR22pm4vLCSmFQ1rt5/tree/docs/configuring-cap.md#troubleshooting) on the role's documentation for details.
