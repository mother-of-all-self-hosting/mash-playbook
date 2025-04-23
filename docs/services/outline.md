<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Outline

[Outline](https://www.getoutline.com/) is an open-source knowledge base for growing teams.


## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# outline                                                              #
#                                                                      #
########################################################################

outline_enabled: true

outline_hostname: outline.example.com

# This must be generated with: `openssl rand -hex 32`
outline_environment_variable_secret_key: ''

# The configuration below connects Outline to the Valkey instance, for session storage purposes.
# You may wish to run a separate Valkey instance for Outline, because Valkey is not multi-tenant.
# Read more in docs/services/valkey.md.
outline_redis_hostname: "{{ valkey_identifier if valkey_enabled else '' }}"

outline_container_additional_networks_custom: |
  {{
    [valkey_container_network]
  }}

# By default, files are stored locally.
# To use another file storage provider, see the "File Storage" section below.

# At least one authentication method MUST be enabled for Outline to work.
# See the "Authentication" section below.

########################################################################
#                                                                      #
# /outline                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting Outline under a subpath (by configuring the `outline_path_prefix` variable) does not seem to be possible due to Outline's technical limitations.

### File Storage

Outline supports multiple [file storage](https://docs.getoutline.com/s/hosting/doc/file-storage-N4M0T6Ypu7) mechanisms.

The default configuration stores files locally in a `data` directory, but you can also stores files on AWS S3 (or [compatible S3 altenative](https://docs.getoutline.com/s/hosting/doc/file-storage-N4M0T6Ypu7#h-s3-compatible-services)).

To enable S3 storage, add the following to your `vars.yml` configuration:

```yml
outline_environment_variable_file_storage: s3

outline_environment_variable_aws_access_key_id: ''
outline_environment_variable_aws_secret_access_key: ''
outline_environment_variable_aws_region: eu-central-1 # example
outline_environment_variable_aws_s3_upload_bucket_url: https://OUTLINE_ASSETS_BUCKET_NAME.s3.eu-central-1.amazonaws.com
outline_environment_variable_aws_s3_upload_bucket_name: OUTLINE_ASSETS_BUCKET_NAME
outline_environment_variable_aws_s3_force_path_style: false
```

### Authentication

For Outline to work, at least one [authentication method](https://docs.getoutline.com/s/hosting/doc/authentication-7ViKRmRY5o) must be enabled.

The Outline Ansible role provides dedicated Ansible variables for configuring these authentication methods via environment variables (see the `outline_environment_variable_*` variables in [`defaults/main.yml` of ansible-role-outline](https://github.com/mother-of-all-self-hosting/ansible-role-outline/blob/main/defaults/main.yml)).

If you need to pass additional environment variables to Outline, for which dedicated Ansible variables are not available, you can use `outline_environment_variables_additional_variables`.

If you define SMTP settings (see the `outline_environment_variable_smtp_*` variables in `defaults/main.yml`), the [Email magic link](https://docs.getoutline.com/s/hosting/doc/email-magic-link-N2CPh5tmTS) authentication method will be enabled:

Unfortunately, even with SMTP settings being defined, we haven't been able to get Outline to succesfully send emails just yet, hitting issues similar to [this one](https://github.com/outline/outline/discussions/2605).

### Configure Valkey

Outline requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Outline is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Outline or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Outline.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Outline, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Outline.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-outline-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-outline-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-outline-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-outline-valkey` instance on the new host, setting `/mash/outline-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Outline.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-outline-'
mash_playbook_service_base_directory_name_prefix: 'outline-'

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
# outline                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point outline to its dedicated Valkey instance
outline_config_redis_hostname: mash-outline-valkey

# Make sure the outline ervice (mash-outline.service) starts after its dedicated Valkey service
outline_systemd_required_services_list_custom:
  - "mash-outline-valkey.service"

# Make sure the outline service (mash-outline.service) is connected to the container network of its dedicated Valkey service
outline_api_container_additional_networks_custom:
  - "mash-outline-valkey"

########################################################################
#                                                                      #
# /outline                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-outline-valkey`.

#### Setting up a shared Valkey instance

If you host only Outline on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Outline to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# outline                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point outline to the shared Valkey instance
outline_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the outline API service (mash-outline.service) starts after the shared Valkey service
outline_api_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the outline API service (mash-outline.service) is connected to the container network of the shared Valkey service
outline_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /outline                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Outline, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-outline-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your Outline instance becomes available at the URL specified with `outline_hostname`.
