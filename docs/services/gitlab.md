<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# GitLab

The playbook can install and configure [GitLab](https://about.gitlab.com/) for you.

GitLab is a complete DevOps platform: Git repository management, code reviews, issue tracking, CI/CD, a container registry and more, in a single application.

See the project's [documentation](https://docs.gitlab.com/) to learn what GitLab does and why it might be useful to you.

For details about configuring the [Ansible role for GitLab](https://github.com/spatterIight/ansible-role-gitlab), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md) online
- 📁 `roles/galaxy/gitlab/docs/configuring-gitlab.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> GitLab is considerably more resource-intensive than most services. It needs at least 4 GB of RAM (8 GB is recommended). Refer to [this page](https://docs.gitlab.com/install/requirements/) for details.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) database — GitLab will default to the Postgres server bundled in its container image if Postgres is not enabled
- (optional) [Valkey](valkey.md) data-store; see [below](#configuring-valkey-optional) for details about installation
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gitlab                                                               #
#                                                                      #
########################################################################

gitlab_enabled: true

gitlab_hostname: gitlab.example.com

########################################################################
#                                                                      #
# /gitlab                                                              #
#                                                                      #
########################################################################
```

If [Postgres](postgres.md) and [exim-relay](exim-relay.md) are enabled on the playbook, GitLab is wired to them automatically. With Postgres, a Postgres extension needs to be created by hand, and some of the Postgres server's settings need adjusting. Refer to [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#using-an-external-postgres-server) on the role's documentation for details.

Refer to [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings such as setting the password for the `root` user, enabling Git over SSH, and enabling the container registry.

### Configuring Valkey (optional)

GitLab uses the Redis server bundled in its container image by default. Optionally, it can use a Valkey instance instead. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If GitLab is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with GitLab or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [Funkwhale](funkwhale.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to GitLab.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for GitLab, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*Refer to [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for GitLab.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-gitlab-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-gitlab-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-gitlab-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-gitlab-valkey` instance on the new host, setting `/mash/gitlab-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of GitLab.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-gitlab-'
mash_playbook_service_base_directory_name_prefix: 'gitlab-'

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
# gitlab                                                               #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point GitLab to its dedicated Valkey instance
gitlab_redis_hostname: mash-gitlab-valkey

# Make sure the GitLab container is connected to the container network of its dedicated Valkey service (mash-gitlab-valkey)
gitlab_container_additional_networks_custom:
  - "mash-gitlab-valkey"

# Make sure the GitLab service (mash-gitlab.service) starts after its dedicated Valkey service (mash-gitlab-valkey.service)
gitlab_systemd_required_services_list_custom:
  - "mash-gitlab-valkey.service"

########################################################################
#                                                                      #
# /gitlab                                                              #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-gitlab-valkey`.

#### Setting up a shared Valkey instance

If you host only GitLab on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook GitLab to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# gitlab                                                               #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point GitLab to the shared Valkey instance
gitlab_redis_hostname: "{{ valkey_identifier }}"

# Make sure the GitLab container is connected to the container network of the shared Valkey service (mash-valkey)
gitlab_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

# Make sure the GitLab service (mash-gitlab.service) starts after the shared Valkey service (mash-valkey.service)
gitlab_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /gitlab                                                              #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for GitLab, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-gitlab-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the GitLab instance becomes available at the URL specified with `gitlab_hostname`. With the configuration above, the service is hosted at `https://gitlab.example.com`.

GitLab reconfigures itself every time it starts, so it may take a few minutes until it becomes reachable.

To get started, open the URL with a web browser, and log in with the username `root`. Refer to [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#set-the-password-for-the-root-user-optional-recommended) on the role's documentation for details about its password.

>[!WARNING]
> By default, GitLab allows anyone to register an account, though new accounts need to be approved by an administrator. If you do not want this, disable sign-ups in the **Admin area** under **Settings** → **General** → **Sign-up restrictions** right after installing.

See [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#backing-up-gitlab) on the role's documentation for details about backing up the instance, and [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#upgrading-gitlab) about upgrading it.

## Related services

- [Forgejo](forgejo.md) — Software forge (Git hosting service, etc.)
- [Gitea](gitea.md) — Software forge (Git hosting service, etc.)
- [Radicle node](radicle-node.md) — Network daemon for the [Radicle](https://radicle.dev/) network, a peer-to-peer code collaboration stack built on Git
