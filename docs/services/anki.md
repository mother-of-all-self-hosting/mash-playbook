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

# Anki

The playbook can install and configure [a synchronization server](https://github.com/ankitects/anki/tree/main/docs/syncserver) for [Anki](https://apps.ankiweb.net) for you.

Anki is a flashcard program that helps you spend more time on challenging material, and less on what you already know. The playbook enables to run a self-hosted synchronization server, similar to what AnkiWeb.net offers.

See the project's [documentation](https://docs.ankiweb.net/sync-server.html) to learn what the synchronization server does and why it might be useful to you.

For details about configuring the [Ansible role for the server](https://github.com/mother-of-all-self-hosting/ansible-role-anki), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-anki/blob/main/docs/configuring-anki.md) online
- 📁 `roles/galaxy/anki/docs/configuring-anki.md` locally, if you have [fetched the Ansible roles](../installing.md)

✨ Anki (暗記) means "Memorize" in Japanese.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# anki                                                                 #
#                                                                      #
########################################################################

anki_enabled: true

anki_hostname: mash.example.com
anki_path_prefix: /anki

########################################################################
#                                                                      #
# /anki                                                                #
#                                                                      #
########################################################################
```

### Set the username and password

You also need to create a user to log in to the instance with a client application. To create one, add the following configuration to your `vars.yml` file. Make sure to replace `YOUR_USERNAME_HERE` and `YOUR_PASSWORD_HERE`.

```yaml
anki_environment_variables_username: YOUR_USERNAME_HERE
anki_environment_variables_password: YOUR_PASSWORD_HERE
```

**Note**: if the username is changed after creating the user, a new user with the specified username will be created by running the installation command, instead of renaming the user.

### Mount a directory for storing data

The service requires a Docker volume to be mounted, so that the directory for storing files is shared with the host machine.

To add the volume, prepare a directory on the host machine and add the following configuration to your `vars.yml` file, setting the directory path to `src`:

```yaml
anki_container_additional_volumes:
  - type: bind
    src: /path/on/the/host
    dst: /data
    options:
```

Make sure permissions of the directory specified to `src` (`/path/on/the/host`).

## Usage

After installation, the synchronization server becomes available at the URL specified with `anki_hostname` and `anki_path_prefix`.

If the instance is served under the subpath, make sure to include a trailing slash when configuring Anki (`mash.example.com/anki/`). See [here](https://docs.ankiweb.net/sync-server.html#reverse-proxies) for more information.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-anki/blob/main/docs/configuring-anki.md#troubleshooting) on the role's documentation for details.
