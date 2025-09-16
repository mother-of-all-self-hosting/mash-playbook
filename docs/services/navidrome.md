<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Navidrome

[Navidrome](https://www.navidrome.org/) is a [Subsonic-API](http://www.subsonic.org/pages/api.jsp) compatible music server.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

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

# By default, Navidrome will look at the /music directory for music files,
# controlled by the `navidrome_environment_variable_nd_musicfolder` variable.
#
# You'd need to mount some music directory into the Navidrome container, like shown below.
# The "Syncthing integration" section below may be relevant.
# navidrome_container_additional_volumes:
#   - type: bind
#     src: /on-host/path/to/music
#     dst: /music
#     options: readonly

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

### Syncthing integration

If you've got a [Syncthing](syncthing.md) service running, you can use it to synchronize your music directory onto the server and then mount it as read-only into the Navidrome container.

We recommend that you make use of the [aux](auxiliary.md) role to create some shared directory like this:

```yaml
########################################################################
#                                                                      #
# aux                                                                  #
#                                                                      #
########################################################################

aux_directory_definitions:
  - dest: "{{ mash_playbook_base_path }}/storage"
  - dest: "{{ mash_playbook_base_path }}/storage/music"

########################################################################
#                                                                      #
# /aux                                                                 #
#                                                                      #
########################################################################
```

You can then mount this `{{ mash_playbook_base_path }}/storage/music` directory into the Syncthing container and synchronize it with some other computer:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

# Other Syncthing configuration..

syncthing_container_additional_volumes:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: /music

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

Finally, mount the `{{ mash_playbook_base_path }}/storage/music` directory into the Navidrome container as read-only:

```yaml
########################################################################
#                                                                      #
# navidrome                                                            #
#                                                                      #
########################################################################

# Other Navidrome configuration..

navidrome_container_additional_volumes:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: /music
    options: readonly

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Navidrome instance becomes available at the URL specified with `navidrome_hostname` and `navidrome_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/navidrome`.

To get started, open the URL with a web browser, and register the administrator account. You can create additional users (admin-privileged or not) after that.

You can also connect various Subsonic-API-compatible [apps](https://www.navidrome.org/docs/overview/#apps) (desktop, web, mobile) to your Navidrome instance.


## Recommended other services

- [Syncthing](syncthing.md) — a continuous file synchronization program which synchronizes files between two or more computers in real time. See [Syncthing integration](#syncthing-integration)
