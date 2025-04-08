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

# Send

The playbook can install and configure [Send](https://github.com/timvisee/send) for you.

Send is a fork of Mozilla's discontinued [Firefox Send](https://github.com/mozilla/send) which allows you to send files to others with a link. Files are end-to-end encrypted so they cannot be read by the server, and also can be protected with a password.

See the project's [documentation](https://github.com/timvisee/send/blob/master/README.md) to learn what Send does and why it might be useful to you.

For details about configuring the [Ansible role for Send](https://github.com/mother-of-all-self-hosting/ansible-role-send), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-send/blob/main/docs/configuring-send.md) online
- 📁 `roles/galaxy/send/docs/configuring-send.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# send                                                                 #
#                                                                      #
########################################################################

send_enabled: true

send_hostname: send.example.com

########################################################################
#                                                                      #
# /send                                                                #
#                                                                      #
########################################################################
```

**Note**: hosting Send under a subpath (by configuring the `send_path_prefix` variable) does not seem to be possible due to Send's technical limitations.

### Configure a storage backend

The service provides these storage backend options: local filesystem (default), Amazon S3 compatible object storage, and Google Cloud Storage.

With the default configuration, the directory for storing files inside the Docker container is set to `/uploads`. You can change it by adding and adjusting the following configuration to your `vars.yml` file:

```yaml
send_environment_variable_file_dir: YOUR_DIRECTORY_HERE
```

**By default this role removes uploaded files when uninstalling the service**. In order to make those files persistent, you need to add a Docker volume to mount in the container, so that the directory for storing files is shared with the host machine.

To add the volume, prepare a directory on the host machine and add the following configuration to your `vars.yml` file, setting the directory path to `src`:

```yaml
send_container_additional_volumes:
  - type: bind
    src: /path/on/the/host
    dst: "{{ send_environment_variable_file_dir }}"
    options:
```

Make sure permissions of the directory specified to `src` (`/path/on/the/host`).

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-send/blob/main/docs/configuring-send.md#configure-a-storage-backend) on the role's documentation for details about how to set up Amazon S3 compatible object storage and Google Cloud Storage.

### Configure upload and download limits (optional)

You can also configure settings for uploading and downloading limits (such as the maximum upload file size and number of the download, as well as expiry time).

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-send/blob/main/docs/configuring-send.md#configure-upload-and-download-limits-optional) on the role's documentation for details about how to set up.

**To mitigate the risk of your server being overwhelmed by legal / illegal use, it is important to set proper limits for the server.** For example, if you intend to use the Send instance for sending relatively small files to a small group of your friends or family, then you can make the default limits stricter as below:

```yaml
# Set maximum upload file size to 100 MB (default: 2 GB, 2147483648 in bytes)
send_environment_variable_max_file_size: 104857600

# Set maximum upload expiry time to 2 days (default: 7 days, 604800 seconds)
send_environment_variable_max_expire_seconds: 172800

# Set maximum number of downloads to 10 (default: 20)
send_environment_variable_max_downloads: 10
```

💡 If your server does not have enough free disk space or you are worried about it, it is worth considering to use cloud storage instead of the local filesystem.

### Configure Valkey

Send requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Send is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Send or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [SearXNG](searxng.md)), it is recommended to install a Valkey instance dedicated to Send.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Send, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Send.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-send-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-send-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-send-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-send-valkey` instance on the new host, setting `/mash/send-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Send.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-send-'
mash_playbook_service_base_directory_name_prefix: 'send-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################
```

##### Edit the main `vars.yml` file

Having configured `vars.yml` for the dedicated instance, add the following configuration to `vars.yml` for the main host, whose path should be `inventory/host_vars/mash.example.com/vars.yml` (replace `mash.example.com` with yours).

```yaml
########################################################################
#                                                                      #
# send                                                                 #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Send to its dedicated Valkey instance
send_config_redis_hostname: mash-send-valkey

# Make sure the Send service (mash-send.service) starts after its dedicated Valkey service (mash-send-valkey.service)
send_systemd_required_services_list_custom:
  - "mash-send-valkey.service"

# Make sure the Send service (mash-send.service) is connected to the container network of its dedicated Valkey service (mash-send-valkey)
send_container_additional_networks_custom:
  - "mash-send-valkey"

########################################################################
#                                                                      #
# /send                                                                #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-send-valkey`.

#### Setting up a shared Valkey instance

If you host only Send on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Send to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

```yaml
########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# send                                                                 #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Send to the shared Valkey instance
send_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Send service (mash-send.service) starts after its dedicated Valkey service (mash-send-valkey.service)
send_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Send container is connected to the container network of its dedicated Valkey service (mash-send-valkey)
send_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /send                                                                #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Send, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-send-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your Send instance becomes available at the URL specified with `send_hostname` and `send_path_prefix`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-send/blob/main/docs/configuring-send.md#usage) on the role's documentation for details about its [CLI client](https://github.com/timvisee/ffsend). The instruction to takedown illegal materials is also available [here](https://github.com/mother-of-all-self-hosting/ansible-role-send/blob/main/docs/configuring-send.md#takedown-illegal-materials).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-send/blob/main/docs/configuring-send.md#troubleshooting) on the role's documentation for details.
