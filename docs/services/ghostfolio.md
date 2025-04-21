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

# Docmost

The playbook can install and configure [Docmost](https://docmost.com/) for you.

Docmost is an free and open-source collaborative wiki and documentation software, designed for seamless real-time collaboration. It can be used to manage a wiki, a knowledge base, project documentation, etc. It has various functions such as granular permissions management system, page history to track changes of articles, etc. It also supports diagramming tools like Draw.io, Excalidraw and Mermaid.

See the project's [documentation](https://docmost.com/docs/) to learn what Docmost does and why it might be useful to you.

For details about configuring the [Ansible role for Docmost](https://github.com/mother-of-all-self-hosting/ansible-role-docmost), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-docmost/blob/main/docs/configuring-docmost.md) online
- 📁 `roles/galaxy/docmost/docs/configuring-docmost.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> - The role is based on Node.js docker image, and is currently expected to run with uid 1000.
> - Excalidraw is available on the playbook. See [here](excalidraw.md) for details about how to install it.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Postgres](postgres.md) database
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation
- (optional) [exim-relay](exim-relay.md) mailer — required on the default configuration

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# docmost                                                              #
#                                                                      #
########################################################################

docmost_enabled: true

docmost_hostname: docmost.example.com

########################################################################
#                                                                      #
# /docmost                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting Docmost under a subpath (by configuring the `docmost_path_prefix` variable) does not seem to be possible due to Docmost's technical limitations.

### Configure a storage backend

The service provides these storage backend options: local filesystem (default) and Amazon S3 compatible object storage.

If local filesystem is used, **this role by default removes uploaded files when uninstalling the service**. In order to make those files persistent, you need to add a Docker volume to mount in the container, so that the directory for storing files is shared with the host machine.

To add the volume, prepare a directory on the host machine and add the following configuration to your `vars.yml` file, setting the directory path to `src`:

```yaml
docmost_data_path: /path/on/the/host
```

Make sure permissions of the directory specified to `src` (`/path/on/the/host`).

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-docmost/blob/main/docs/configuring-docmost.md#configure-a-storage-backend) on the role's documentation for details about how to set up Amazon S3 compatible object storage for Docmost.

### Configure the mailer

You can configure a mailer for functions such as user invitation. Docmost supports a SMTP server and Postmark.

**You can use exim-relay as the mailer, which is enabled on this playbook by default.** If you enable exim-relay on the playbook and will use it for Docmost, you do not have to add settings for them, as Docmost is wired to the mailer automatically. See [here](exim-relay.md) for details about how to set it up.

If you will use another SMTP server or Postmark, see [this section](https://github.com/mother-of-all-self-hosting/ansible-role-docmost/blob/main/docs/configuring-docmost.md#configure-the-mailer) on the role's documentation for details about configuring the mailer.

If you do not want to enable a mailer for Docmost altogether, add the following configuration to your `vars.yml` file:

```yaml
docmost_mailer_enabled: false
```

### Configure Valkey

Docmost requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Docmost is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Docmost or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Docmost.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Docmost, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Docmost.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-docmost-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-docmost-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-docmost-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-docmost-valkey` instance on the new host, setting `/mash/docmost-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Docmost.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-docmost-'
mash_playbook_service_base_directory_name_prefix: 'docmost-'

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
# docmost                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Docmost to its dedicated Valkey instance
docmost_config_redis_hostname: mash-docmost-valkey

# Make sure the Docmost service (mash-docmost.service) starts after its dedicated Valkey service (mash-docmost-valkey.service)
docmost_systemd_required_services_list_custom:
  - "mash-docmost-valkey.service"

# Make sure the Docmost service (mash-docmost.service) is connected to the container network of its dedicated Valkey service (mash-docmost-valkey)
docmost_container_additional_networks_custom:
  - "mash-docmost-valkey"

########################################################################
#                                                                      #
# /docmost                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-docmost-valkey`.

#### Setting up a shared Valkey instance

If you host only Docmost on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Docmost to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# docmost                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Docmost to the shared Valkey instance
docmost_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Docmost service (mash-docmost.service) starts after its dedicated Valkey service (mash-docmost-valkey.service)
docmost_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Docmost container is connected to the container network of its dedicated Valkey service (mash-docmost-valkey)
docmost_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /docmost                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Enable Telemetry (optional)

By default this playbook disables Docmost's [telemetry](https://docmost.com/docs/self-hosting/environment-variables#telemetry) which collects information about the active version, user count, page count, space and workspace count, and sends to the Docmost server (see [here](https://github.com/docmost/docmost/blob/main/apps/server/src/integrations/telemetry/telemetry.service.ts)).

If you are fine with sending such infomation and want to help developers, add the following configuration to your `vars.yml` file:

```yaml
docmost_environment_variable_disable_telemetry: false
```

## Installation

If you have decided to install the dedicated Valkey instance for Docmost, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-docmost-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your Docmost instance becomes available at the URL specified with `docmost_hostname`.

To get started, go to the URL on a web browser and create a first workspace by inputting required information. For an email address, make sure to input your own email address, not the one of the mailer.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-docmost/blob/main/docs/configuring-docmost.md#troubleshooting) on the role's documentation for details.
