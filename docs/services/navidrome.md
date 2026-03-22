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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Navidrome

The playbook can install and configure [Navidrome](https://www.navidrome.org/) for you.

Navidrome is a [Subsonic-API](http://www.subsonic.org/pages/api.jsp) compatible music server.

See the project's [documentation](https://www.navidrome.org/docs/) to learn what Navidrome does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# navidrome                                                            #
#                                                                      #
########################################################################

navidrome_enabled: true

navidrome_hostname: mash.example.com
navidrome_path_prefix: /navidrome

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

### File management

Since Navidrome is just a music player, you would need to prepare music files to be played with it.

If your server runs a file management service along with Navidrome such as [File Browser](filebrowser.md), [FileBrowser Quantum](filebrowser-quantum.md), and [Syncthing](syncthing.md), it is possible to upload files to the server or synchronize your music directory with it to make them accessible on Navidrome.

#### Preparing directories

First, let's create a directory to be shared with the services. You can make use of the [aux](auxiliary.md) role by adding the following configuration to your `vars.yml` file. We create two directories here; the directory to be shared among Navidrome and other services, and its parent directory. If you are willing to have other services share directories, you can add another path by adding one to the list:

```yaml
########################################################################
#                                                                      #
# aux                                                                  #
#                                                                      #
########################################################################

aux_directory_definitions:
  - dest: "{{ mash_playbook_base_path }}/storage"
  - dest: "{{ mash_playbook_base_path }}/storage/music"
# - dest: another shared directory path …

########################################################################
#                                                                      #
# /aux                                                                 #
#                                                                      #
########################################################################
```

#### Mounting the directory into the Navidrome container

Next, mount the `{{ mash_playbook_base_path }}/storage/music` directory into the Navidrome container. By default, Navidrome will look at the `/music` directory for music files, controlled by the `navidrome_environment_variable_nd_musicfolder` variable.

>[!NOTE]
> The directory may be mounted as read-only to prevent data inside the directory from accidentally being deleted or modified by Navidrome.

```yaml
########################################################################
#                                                                      #
# navidrome                                                            #
#                                                                      #
########################################################################

# Other Navidrome configuration …

navidrome_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: "{{ navidrome_environment_variable_nd_musicfolder }}"
    options: readonly

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

#### Sharing the directory with other containers

You can then mount this `{{ mash_playbook_base_path }}/storage/music` directory on other service's container.

For example, adding the configuration below will let you to access to `/music` directory on the File Browser's UI, so that you can upload files to the server directly and make them accessible on Navidrome:

```yaml
########################################################################
#                                                                      #
# filebrowser                                                          #
#                                                                      #
########################################################################

# Other File Browser configuration …

filebrowser_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: "/srv/music"

########################################################################
#                                                                      #
# /filebrowser                                                         #
#                                                                      #
########################################################################
```

Adding the configuration below makes it possible for the Syncthing service to synchronize the directory with other computers:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

# Other Syncthing configuration …

syncthing_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: /music

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Navidrome instance becomes available at the URL specified with `navidrome_hostname` and `navidrome_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/navidrome`.

To get started, open the URL with a web browser to create an administrator account. You can create additional users (admin-privileged or not) after that.

You can also connect various Subsonic-API-compatible [apps](https://www.navidrome.org/docs/overview/#apps) (desktop, web, mobile) to your Navidrome instance.

## Related services

- [Feishin](feishin.md) — Music player for Navidrome, Jellyfin, Funkwhale, etc.
