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

# Polaris

The playbook can install and configure [Polaris](https://github.com/agersant/polaris) for you.

Polaris is a music streaming server with a player to enjoy your music collection from any computer or mobile device.

See the project's [documentation](https://github.com/agersant/polaris/blob/master/README.md) to learn what Polaris does and why it might be useful to you.

For details about configuring the [Ansible role for Polaris](https://radicle.network/nodes/iris.radicle.network/rad%3Az49EpGUPcp76sUQ4udcz7pBRPuq7u), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az49EpGUPcp76sUQ4udcz7pBRPuq7u/tree/docs/configuring-polaris.md) online
- 📁 `roles/galaxy/polaris/docs/configuring-polaris.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# polaris                                                              #
#                                                                      #
########################################################################

polaris_enabled: true

polaris_hostname: polaris.example.com

########################################################################
#                                                                      #
# /polaris                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting Polaris under a subpath (by configuring the `polaris_path_prefix` variable) does not seem to be possible due to Polaris's technical limitations.

### File management

If your server runs a file management service along with Polaris such as [File Browser](filebrowser.md), [FileBrowser Quantum](filebrowser-quantum.md), and [Syncthing](syncthing.md), it is possible to upload files to the server or synchronize your music directory with it to make them accessible on Polaris.

#### Preparing directories

First, let's create a directory to be shared with the services. You can make use of the [aux](auxiliary.md) role by adding the following configuration to your `vars.yml` file. We create two directories here; the directory to be shared among Polaris and other services, and its parent directory. If you are willing to have other services share directories, you can add another path by adding one to the list:

```yaml
########################################################################
#                                                                      #
# aux                                                                  #
#                                                                      #
########################################################################

aux_directory_definitions:
  - dest: "{{ mash_playbook_base_path }}/storage"
  - dest: "{{ mash_playbook_base_path }}/storage/polaris"
# - dest: another shared directory path …

########################################################################
#                                                                      #
# /aux                                                                 #
#                                                                      #
########################################################################
```

#### Mounting the directory into the Polaris container

Next, mount the `{{ mash_playbook_base_path }}/storage/polaris` directory into the Polaris container.

>[!NOTE]
> The directory is mounted as writable to enable data modification and deletion by Polaris.

```yaml
########################################################################
#                                                                      #
# polaris                                                              #
#                                                                      #
########################################################################

# Other Polaris configuration …

polaris_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/polaris"
    dst: /music

########################################################################
#                                                                      #
# /polaris                                                             #
#                                                                      #
########################################################################
```

#### Sharing the directory with other containers

You can then mount this `{{ mash_playbook_base_path }}/storage/polaris` directory on other service's container.

For example, adding the configuration below will let you to access to `/polaris` directory on the File Browser's UI, so that you can upload files to the server directly and make them accessible on Polaris:

```yaml
########################################################################
#                                                                      #
# filebrowser                                                          #
#                                                                      #
########################################################################

# Other File Browser configuration …

filebrowser_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/polaris"
    dst: "/srv/polaris"

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

syncthing_container_additional_volumes:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/polaris"
    dst: /polaris

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Polaris instance becomes available at the URL specified with `polaris_hostname`. With the configuration above, the service is hosted at `https://polaris.example.com`.

To get started, open the URL with a web browser, and register the account. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az49EpGUPcp76sUQ4udcz7pBRPuq7u/tree/docs/configuring-polaris.md#troubleshooting) on the role's documentation for details.

## Related services

- [Navidrome](navidrome.md) — Subsonic-API compatible music server
