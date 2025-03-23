<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Infisical

[Infisical](https://infisical.com/) is an open-source end-to-end encrypted platform for securely managing secrets and configs across your team, devices, and infrastructure.


## Dependencies

This service requires the following other services:

- a [MongoDB](mongodb.md) document-oriented database server
- a [Traefik](traefik.md) reverse-proxy server
- a [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation


## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# infisical                                                            #
#                                                                      #
########################################################################

infisical_enabled: true

infisical_hostname: infisical.example.com

# Generate this with: `openssl rand -hex 16`
infisical_backend_environment_variable_encryption_key: ''

# WARNING: uncomment this after creating your first user account,
# unless you'd like to run a server with public registration enabled.
# infisical_backend_environment_variable_invite_only_signup: true

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting Infisical under a subpath (by configuring the `infisical_path_prefix` variable) does not seem to be possible right now, due to Infisical limitations.

### Configure Valkey

Infisical requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Infisical is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Infisical or you have already set up services which need Valkey, it is recommended to install a Valkey instance dedicated to Infisical. See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Infisical, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Infisical. See [here](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) for details.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-infisical-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-infisical-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-infisical-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-infisical-valkey` instance on the new host, setting `/mash/infisical-valkey` to the base directory of the dedicated Valkey instance.

**Notes**:
- As this `vars.yml` file will be used for the new host, make sure to set `mash_playbook_generic_secret_key`. It does not need to be same as the one on `vars.yml` for the main host. Without setting it, the Valkey instance will not be configured.
- Since these variables are used to configure the service name and directory path of the Valkey instance, you do not have to have them matched with the hostname of the server. For example, even if the hostname is `www.example.com`, you do **not** need to set `mash_playbook_service_base_directory_name_prefix` to `www-`. If you are not sure which string you should set, you might as well use the values as they are.

```yaml
---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-infisical-'
mash_playbook_service_base_directory_name_prefix: 'infisical-'

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
# infisical                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Infisical to its dedicated Valkey instance
infisical_environment_variable_redis_host: mash-infisical-valkey
infisical_environment_variable_redis_cache_host: mash-infisical-valkey

# Make sure the Infisical service (mash-infisical.service) starts after its dedicated Valkey service (mash-infisical-valkey.service)
infisical_systemd_required_services_list_custom:
  - "mash-infisical-valkey.service"

# Make sure the Infisical container is connected to the container network of its dedicated Valkey service (mash-infisical-valkey)
infisical_container_additional_networks_custom:
  - "mash-infisical-valkey"

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-infisical-valkey`.

#### Setting up a shared Valkey instance

If you host only Infisical on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Infisical to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# infisical                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Infisical to the shared Valkey instance
infisical_environment_variable_redis_host: "{{ valkey_identifier }}"
infisical_environment_variable_redis_cache_host: "{{ valkey_identifier }}"

# Make sure the Infisical service (mash-infisical.service) starts after the shared Valkey service (mash-valkey.service)
infisical_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Infisical container is connected to the container network of the shared Valkey service (mash-valkey)
infisical_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Configure authentication

By default, the Infisical instance allows anyone to sign up from the web interface.

We recommend installing with registration open to public at first to create your first user. After creating the user, you can disable public registration by adding the following configuration to `vars.yml`:

```yaml
infisical_backend_environment_variable_invite_only_signup: true
```

Note that enabling invite-only registration requires the mailer to be configured with the settings below.

### Configure the mailer

As described in the Infisical documentation about [email](https://infisical.com/docs/self-hosting/configuration/email), Infisical requires the mailer (SMTP server) for important functionality such as user registration.

To enable the mailer function, add the following configuration to your `vars.yml` file:

```yaml
infisical_backend_environment_variable_smtp_host: smtp.example.com
infisical_backend_environment_variable_smtp_port: 587
infisical_backend_environment_variable_smtp_secure: false

infisical_backend_environment_variable_smtp_username: infisical@example.com
infisical_backend_environment_variable_smtp_password: ''

infisical_backend_environment_variable_smtp_address: infisical@example.com
infisical_backend_environment_variable_smtp_name: Infisical
```

For additional SMTP-related variables, consult the [`defaults/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-infisical/blob/main/defaults/main.yml) in the [ansible-role-infisical](https://github.com/mother-of-all-self-hosting/ansible-role-infisical) Ansible role.

**Notes**:
- **You can use exim-relay as the mailer, which is enabled on this playbook by default.** See [here](exim-relay.md) for details about how to set it up.
- Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

## Installation

If you have decided to install the dedicated Valkey instance for Infisical, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-infisical-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) for more details about it.

## Usage

After installation, your Infisical instance becomes available at the URL specified with `infisical_hostname`.

To log in to the service and get started, you need to create a user from the web interface.

After creating the first user, you can prevent others from registering by making registration invite-only. To do so, configure [authentication](#configure-authentication) and re-run the playbook: `just install-service infisical`
