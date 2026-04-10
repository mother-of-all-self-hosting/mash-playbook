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

# HeyForm

The playbook can install and configure [HeyForm](https://github.com/heyform/heyform) for you.

HeyForm is a form builder that lets you create, customize, and automate forms.

See the project's [documentation](https://docs.heyform.net/) to learn what HeyForm does and why it might be useful to you.

For details about configuring the [Ansible role for HeyForm](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzsKztkwnLv9wVMRYbcpoFesx6L5j), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzsKztkwnLv9wVMRYbcpoFesx6L5j/tree/docs/configuring-heyform.md) online
- 📁 `roles/galaxy/heyform/docs/configuring-heyform.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [MongoDB](mongodb.md) database
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation
- (optional) [exim-relay](exim-relay.md) mailer — required on the default configuration

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# heyform                                                              #
#                                                                      #
########################################################################

heyform_enabled: true

heyform_hostname: heyform.example.com

########################################################################
#                                                                      #
# /heyform                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting HeyForm under a subpath (by configuring the `heyform_path_prefix` variable) does not seem to be possible due to HeyForm's technical limitations.

### Set a random string

You also need to set a random string to the variable as below by adding the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
heyform_environment_variables_form_encryption_key: YOUR_SECRET_KEY_HERE
```

### Configuring the mailer (optional)

On HeyForm you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Configure Valkey

HeyForm requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If HeyForm is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with HeyForm or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to HeyForm.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for HeyForm, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for HeyForm.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-heyform-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-heyform-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-heyform-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-heyform-valkey` instance on the new host, setting `/mash/heyform-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of HeyForm.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-heyform-'
mash_playbook_service_base_directory_name_prefix: 'heyform-'

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
# heyform                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point HeyForm to its dedicated Valkey instance
heyform_redis_hostname: mash-heyform-valkey

# Make sure the HeyForm service (mash-heyform.service) is connected to the container network of its dedicated Valkey service (mash-heyform-valkey)
heyform_container_additional_networks_custom:
  - "mash-heyform-valkey"

# Make sure the HeyForm service (mash-heyform.service) starts after its dedicated Valkey service (mash-heyform-valkey.service)
heyform_systemd_required_services_list_custom:
  - "mash-heyform-valkey.service"

########################################################################
#                                                                      #
# /heyform                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-heyform-valkey`.

#### Setting up a shared Valkey instance

If you host only HeyForm on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook HeyForm to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# heyform                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point HeyForm to the shared Valkey instance
heyform_redis_hostname: "{{ valkey_identifier }}"

# Make sure the HeyForm container is connected to the container network of the shared Valkey service (mash-valkey)
heyform_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

# Make sure the HeyForm service (mash-heyform.service) starts after the shared Valkey service (mash-valkey.service)
heyform_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /heyform                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for HeyForm, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-heyform-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, the HeyForm instance becomes available at the URL specified with `heyform_hostname`. With the configuration above, the service is hosted at `https://heyform.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzsKztkwnLv9wVMRYbcpoFesx6L5j/tree/docs/configuring-heyform.md#troubleshooting) on the role's documentation for details.

## Related services

- [LimeSurvey](limesurvey.md) — Web based forms and surveys
