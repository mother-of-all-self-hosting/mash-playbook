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

# asciinema server

The playbook can install and configure [asciinema server](https://asciinema_server.com/) for you.

asciinema server is an free and open-source collaborative wiki and documentation software, designed for seamless real-time collaboration. It can be used to manage a wiki, a knowledge base, project documentation, etc. It has various functions such as granular permissions management system, page history to track changes of articles, etc. It also supports diagramming tools like Draw.io, Excalidraw and Mermaid.

See the project's [documentation](https://asciinema_server.com/docs/) to learn what asciinema server does and why it might be useful to you.

For details about configuring the [Ansible role for asciinema server](https://github.com/mother-of-all-self-hosting/ansible-role-asciinema-server), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-asciinema-server/blob/main/docs/configuring-asciinema-server.md) online
- 📁 `roles/galaxy/asciinema_server/docs/configuring-asciinema-server.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> - The role is based on Node.js docker image, and is currently expected to run with uid 1000.
> - Excalidraw is available on the playbook. See [here](excalidraw.md) for details about how to install it.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation
- (optional) [exim-relay](exim-relay.md) mailer — required on the default configuration

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# asciinema_server                                                     #
#                                                                      #
########################################################################

asciinema_server_enabled: true

asciinema_server_hostname: asciinema_server.example.com

########################################################################
#                                                                      #
# /asciinema_server                                                    #
#                                                                      #
########################################################################
```

**Note**: hosting asciinema server under a subpath (by configuring the `asciinema_server_path_prefix` variable) does not seem to be possible due to asciinema server's technical limitations.

### Configure a storage backend

The service provides these storage backend options: local filesystem (default) and Amazon S3 compatible object storage.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-asciinema-server/blob/main/docs/configuring-asciinema-server.md#configure-a-storage-backend) on the role's documentation for details about how to set up Amazon S3 compatible object storage for asciinema server.

### Configure the mailer

You can configure a mailer for functions such as user invitation. asciinema server supports a SMTP server and Postmark.

**You can use exim-relay as the mailer, which is enabled on this playbook by default.** If you enable exim-relay on the playbook and will use it for asciinema server, you do not have to add settings for them, as asciinema server is wired to the mailer automatically. See [here](exim-relay.md) for details about how to set it up.

If you will use another SMTP server or Postmark, see [this section](https://github.com/mother-of-all-self-hosting/ansible-role-asciinema-server/blob/main/docs/configuring-asciinema-server.md#configure-the-mailer) on the role's documentation for details about configuring the mailer.

If you do not want to enable a mailer for asciinema server altogether, add the following configuration to your `vars.yml` file:

```yaml
asciinema_server_mailer_enabled: false
```

### Configure Valkey

asciinema server requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If asciinema server is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with asciinema server or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to asciinema server.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for asciinema server, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for asciinema server.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-asciinema_server-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-asciinema_server-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-asciinema_server-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-asciinema_server-valkey` instance on the new host, setting `/mash/asciinema_server-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of asciinema server.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-asciinema_server-'
mash_playbook_service_base_directory_name_prefix: 'asciinema_server-'

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
# asciinema_server                                                     #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point asciinema server to its dedicated Valkey instance
asciinema_server_redis_hostname: mash-asciinema_server-valkey

# Make sure the asciinema server service (mash-asciinema_server.service) starts after its dedicated Valkey service (mash-asciinema_server-valkey.service)
asciinema_server_systemd_required_services_list_custom:
  - "mash-asciinema_server-valkey.service"

# Make sure the asciinema server service (mash-asciinema_server.service) is connected to the container network of its dedicated Valkey service (mash-asciinema_server-valkey)
asciinema_server_container_additional_networks_custom:
  - "mash-asciinema_server-valkey"

########################################################################
#                                                                      #
# /asciinema_server                                                    #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-asciinema_server-valkey`.

#### Setting up a shared Valkey instance

If you host only asciinema server on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook asciinema server to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# asciinema_server                                                     #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point asciinema server to the shared Valkey instance
asciinema_server_redis_hostname: "{{ valkey_identifier }}"

# Make sure the asciinema server service (mash-asciinema_server.service) starts after its dedicated Valkey service (mash-asciinema_server-valkey.service)
asciinema_server_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the asciinema server container is connected to the container network of its dedicated Valkey service (mash-asciinema_server-valkey)
asciinema_server_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /asciinema_server                                                    #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Enable Telemetry (optional)

By default this playbook disables asciinema server's [telemetry](https://asciinema_server.com/docs/self-hosting/environment-variables#telemetry) which collects information about the active version, user count, page count, space and workspace count, and sends to the asciinema server server (see [here](https://github.com/asciinema_server/asciinema_server/blob/main/apps/server/src/integrations/telemetry/telemetry.service.ts)).

If you are fine with sending such information and want to help developers, add the following configuration to your `vars.yml` file:

```yaml
asciinema_server_environment_variable_disable_telemetry: false
```

## Installation

If you have decided to install the dedicated Valkey instance for asciinema server, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-asciinema_server-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, the asciinema server instance becomes available at the URL specified with `asciinema_server_hostname`. With the configuration above, the service is hosted at `https://asciinema_server.example.com`.

To get started, open the URL with a web browser, and create a first workspace by inputting required information. For an email address, make sure to input your own email address, not the one of the mailer.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-asciinema-server/blob/main/docs/configuring-asciinema-server.md#troubleshooting) on the role's documentation for details.

## Related services

- [Excalidraw](excalidraw.md) — Free and open source virtual whiteboard for sketching hand-drawn like diagrams
