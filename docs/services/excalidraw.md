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

# Excalidraw

The playbook can install and configure [a synchronization server](https://github.com/excalidrawtects/excalidraw/tree/main/docs/syncserver) for [Excalidraw](https://apps.excalidrawweb.net) for you.

Excalidraw is a flashcard program that helps you spend more time on challenging material, and less on what you already know. The playbook enables to run a self-hosted synchronization server, similar to what ExcalidrawWeb.net offers.

See the project's [documentation](https://docs.excalidrawweb.net/sync-server.html) to learn what the synchronization server does and why it might be useful to you.

For details about configuring the [Ansible role for the server](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw/blob/main/docs/configuring-excalidraw.md) online
- 📁 `roles/galaxy/excalidraw/docs/configuring-excalidraw.md` locally, if you have [fetched the Ansible roles](../installing.md)

✨ Excalidraw (暗記) means "Memorize" in Japanese.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# excalidraw                                                           #
#                                                                      #
########################################################################

excalidraw_enabled: true

excalidraw_hostname: mash.example.com
excalidraw_path_prefix: /excalidraw

########################################################################
#                                                                      #
# /excalidraw                                                          #
#                                                                      #
########################################################################
```

### Set the username and password

You also need to create a user to log in to the instance with a client application. To create one, add the following configuration to your `vars.yml` file. Make sure to replace `YOUR_USERNAME_HERE` and `YOUR_PASSWORD_HERE`.

```yaml
excalidraw_environment_variables_username: YOUR_USERNAME_HERE
excalidraw_environment_variables_password: YOUR_PASSWORD_HERE
```

**Note**: if the username is changed after creating the user, a new user with the specified username will be created by running the installation command, instead of renaming the user.

### Mount a directory for storing data

The service requires a Docker volume to be mounted, so that the directory for storing files is shared with the host machine.

To add the volume, prepare a directory on the host machine and add the following configuration to your `vars.yml` file, setting the directory path to `src`:

```yaml
excalidraw_container_additional_volumes:
  - type: bind
    src: /path/on/the/host
    dst: /data
    options:
```

Make sure permissions of the directory specified to `src` (`/path/on/the/host`).

## Usage

After installation, the synchronization server becomes available at the URL specified with `excalidraw_hostname` and `excalidraw_path_prefix`.

If the instance is served under the subpath, make sure to include a trailing slash when configuring Excalidraw (`mash.example.com/excalidraw/`). See [here](https://docs.excalidrawweb.net/sync-server.html#reverse-proxies) for more information.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw/blob/main/docs/configuring-excalidraw.md#troubleshooting) on the role's documentation for details.
