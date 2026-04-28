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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Borg Web UI

The playbook can install and configure [Borg Web UI](https://karanhudia.github.io/borg-ui/) for you.

Borg Web UI is an unofficial web interface for [BorgBackup](https://borgbackup.readthedocs.io/).

See the project's [documentation](https://karanhudia.github.io/borg-ui/) to learn what Borg Web UI does and why it might be useful to you.

For details about configuring the [Ansible role for Borg Web UI](https://radicle.network/nodes/seed.radicle.garden/rad%3AzxNS7XeayGimb4WFfvqmasiZZC3v), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3AzxNS7XeayGimb4WFfvqmasiZZC3v/tree/docs/configuring-borg-ui.md) online
- 📁 `roles/galaxy/borg_ui/docs/configuring-borg-ui.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Apprise API](apprise.md)
- (optional) [Valkey](valkey.md) data-store; see [below](#configure-valkey-optional) for details about installation

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# borg_ui                                                              #
#                                                                      #
########################################################################

borg_ui_enabled: true

borg_ui_hostname: borg-ui.example.com

########################################################################
#                                                                      #
# /borg_ui                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting Borg Web UI under a subpath (by configuring the `borg_ui_path_prefix` variable) does not seem to be possible due to Borg Web UI's technical limitations.

### Configure Valkey (optional)

Valkey can optionally be enabled to improve Borg Web UI's performance on archive browsing. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Borg Web UI is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Borg Web UI or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Borg Web UI.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Borg Web UI, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Borg Web UI.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-borg-ui-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-borg-ui-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-borg-ui-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-borg-ui-valkey` instance on the new host, setting `/mash/borg-ui-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Borg Web UI.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-borg-ui-'
mash_playbook_service_base_directory_name_prefix: 'borg-ui-'

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
# borg_ui                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Make sure the connection via Unix domain socket is enabled
# Set to `false` to enable TCP connection instead
borg_ui_redis_socket_enabled: true

# Connect Borg Web UI to its dedicated Valkey instance via the Unix domain socket
#
# Alternatively, if you set `borg_ui_redis_socket_enabled` to `false`,
# - Add the dedicated Valkey instance (mash-borg-ui-valkey) to `borg_ui_redis_hostname`
# - Add its network (mash-borg-ui-valkey) to `borg_ui_container_additional_networks_custom`
borg_ui_redis_socket_path_host: /mash/borg-ui-valkey/run

# Make sure the Borg Web UI service (mash-borg-ui.service) starts after its dedicated Valkey service (mash-borg-ui-valkey.service)
borg_ui_systemd_required_services_list_custom:
  - "mash-borg-ui-valkey.service"

########################################################################
#                                                                      #
# /borg_ui                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-borg-ui-valkey`.

#### Setting up a shared Valkey instance

If you host only Borg Web UI on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Borg Web UI to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# borg_ui                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Make sure the connection via Unix domain socket is enabled
# Set to `false` to enable TCP connection instead
borg_ui_redis_socket_enabled: true

# Connect Borg Web UI to the shared Valkey instance via the Unix domain socket
#
# Alternatively, if you set `borg_ui_redis_socket_enabled` to `false`,
# - Add the shared Valkey instance (mash-valkey) to `borg_ui_redis_hostname`
# - Add its network (mash-valkey) to `borg_ui_container_additional_networks_custom`
borg_ui_redis_socket_path_host: "{{ valkey_run_path }}"

# Make sure the Borg Web UI service (mash-borg-ui.service) starts after the shared Valkey service (mash-valkey.service)
borg_ui_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /borg_ui                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Integrating with Prometheus (optional)

Borg Web UI can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Borg Web UI and Prometheus do not share a network (like Traefik), you can connect the Borg Web UI container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ borg_ui_container_network }}"
```

#### Expose metrics publicly

If Borg Web UI metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-borg-ui`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
borg_ui_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
borg_ui_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Installation

If you have decided to install the dedicated Valkey instance for Borg Web UI, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-borg-ui-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, the Borg Web UI instance becomes available at the URL specified with `borg_ui_hostname`. With the configuration above, the service is hosted at `https://borg-ui.example.com`.

To get started, open the URL with a web browser to log in to the instance.

Refer to [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3AzxNS7XeayGimb4WFfvqmasiZZC3v/tree/docs/configuring-borg-ui.md#usage) on the role's documentation for more information.

To load a source directory to be backed up inside the container, you can add one to `borg_ui_container_additional_volumes_custom` as below:

```yaml
borg_ui_container_additional_volumes_custom:
  - type: "bind"
    src: /mash
    dst: /local
    options: readonly
```

>[!NOTE]
> The directory should be mounted with `readonly` to prevent accidental modification or ransomware attacks.

### Configuring notification services (optional)

On Borg Web UI you can add configuration settings of notification services. If you enable [Apprise API](apprise.md) in your inventory configuration, the playbook will automatically connect it to the Borg Web UI service.

As the Borg Web UI instance does not support configuring the notification services with environment variables, you can add default options for them on its UI. Refer to [this page](https://karanhudia.github.io/borg-ui/notifications.html) on the official documentation as well about how to configure them.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3AzxNS7XeayGimb4WFfvqmasiZZC3v/tree/docs/configuring-borg-ui.md#troubleshooting) on the role's documentation for details.

## Related services

- [BorgBackup with borgmatic](backup-borg.md) — Deduplicating backup program with optional compression and encryption
- [Duplicati](duplicati.md) — Backup software that securely stores encrypted, incremental, compressed backups on local storage, cloud storage services and remote file servers
