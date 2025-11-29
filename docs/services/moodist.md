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

# Moodist

The playbook can install and configure [Moodist](https://moodist.mvze.net) for you.

Moodist is a free web application to mix and play ambient soundtracks (river, rain, cafe, airport, etc).

See the project's [documentation](https://github.com/remvze/moodist/blob/main/README.md) to learn what Moodist does and why it might be useful to you.

For details about configuring the [Ansible role for Moodist](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Ez9aU119yFMs59cnA3KUnExFAeN), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Ez9aU119yFMs59cnA3KUnExFAeN/tree/docs/configuring-moodist.md) online
- 📁 `roles/galaxy/moodist/docs/configuring-moodist.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# moodist                                                              #
#                                                                      #
########################################################################

moodist_enabled: true

moodist_hostname: moodist.example.com

########################################################################
#                                                                      #
# /moodist                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting Moodist under a subpath (by configuring the `moodist_path_prefix` variable) does not seem to be possible due to Moodist's technical limitations.

### Using the default Docker image (optional)

To have the service run as the playbook's default user instead of root user, this service is by default configured to use the Docker image locally built on [this own Dockerfile](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Ez9aU119yFMs59cnA3KUnExFAeN/tree/51bdebb3210e646fb7e83666b8208d5a820ae0c5/templates/Dockerfile.j2).

If you prefer simply pulling and using [the official Docker image](https://github.com/users/remvze/packages/container/package/moodist) instead, add the following configuration to your `vars.yml` file:

```yaml
moodist_container_image_self_build: false
```

>[!NOTE]
> Adding the variable configures the playbook to run the service as a root user.

## Usage

After running the command for installation, the Moodist instance becomes available at the URL specified with `moodist_hostname`. With the configuration above, the service is hosted at `https://moodist.example.com`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Ez9aU119yFMs59cnA3KUnExFAeN/tree/docs/configuring-moodist.md#troubleshooting) on the role's documentation for details.
