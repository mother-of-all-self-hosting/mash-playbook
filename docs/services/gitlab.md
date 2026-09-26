<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# GitLab

The playbook can install and configure [GitLab](https://about.gitlab.com/) for you.

GitLab is a complete DevOps platform: Git repository management, code reviews, issue tracking, CI/CD, a container registry and more, in a single application. See the project's [documentation](https://docs.gitlab.com/) to learn more.

For details about configuring the [Ansible role for GitLab](https://github.com/spatterIight/ansible-role-gitlab), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md) online
- 📁 `roles/galaxy/gitlab/docs/configuring-gitlab.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> GitLab needs at least 4 GB of RAM (8 GB is recommended). Refer to [this page](https://docs.gitlab.com/install/requirements/) for details.

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

If [Postgres](postgres.md) and [exim-relay](exim-relay.md) are enabled on the playbook, GitLab is wired to them automatically. With Postgres, an extension needs to be created by hand and some server settings adjusted (see [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#using-an-external-postgres-server) on the role's documentation).

See [the role's documentation](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#adjusting-the-playbook-configuration) for other settings, such as the password for the `root` user, Git over SSH and the container registry.

### Configuring Valkey (optional)

GitLab uses the Redis server bundled in its container image by default. Optionally, it can use a [Valkey](valkey.md) instance dedicated to GitLab instead (sharing a Valkey instance among services has security concerns and can cause data conflicts).

To create the dedicated instance, follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*Refer to [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

#### Adjust `hosts`

Add a supplementary host for GitLab to `inventory/hosts`. Replace `mash.example.com` with your hostname, and `YOUR_SERVER_IP_ADDRESS_HERE` with the host's IP address (the same for both, unless Valkey runs on another machine):

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-gitlab-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string. If `[mash_example_com]` already has other entries, add the supplementary host to it.

#### Create `vars.yml` for the dedicated instance

Create `inventory/host_vars/mash.example.com-gitlab-deps/vars.yml` with the content below. Running the playbook then creates the `mash-gitlab-valkey` instance, with `/mash/gitlab-valkey` as its base directory.

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

#### Edit the main `vars.yml` file

Add the following configuration to the main host's `vars.yml` file (`inventory/host_vars/mash.example.com/vars.yml`):

```yaml
########################################################################
#                                                                      #
# gitlab                                                               #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point GitLab to the dedicated Valkey instance
gitlab_redis_hostname: mash-gitlab-valkey

# Connect GitLab to the dedicated Valkey instance's container network
gitlab_container_additional_networks_custom:
  - "mash-gitlab-valkey"

# Start GitLab after the dedicated Valkey instance
gitlab_systemd_required_services_list_custom:
  - "mash-gitlab-valkey.service"

########################################################################
#                                                                      #
# /gitlab                                                              #
#                                                                      #
########################################################################
```

## Installation

If you set up the dedicated Valkey instance, run the [installation](../installing.md) command for the supplementary host (`mash.example.com-gitlab-deps`) before the main host (`mash.example.com`). `just install-all` and `just setup-all` take care of this order (see [here](../running-multiple-instances.md#1-adjust-hosts)).

## Usage

After installation, GitLab becomes available at `gitlab_hostname` (`https://gitlab.example.com` with the configuration above). It reconfigures itself on every start, so it may take a few minutes to become reachable.

Log in with the username `root` (see [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#set-the-password-for-the-root-user-optional-recommended) on the role's documentation for its password).

>[!WARNING]
> By default, anyone can register an account, pending approval by an administrator. To disable sign-ups, go to the **Admin area** → **Settings** → **General** → **Sign-up restrictions** right after installing.

See the role's documentation for [backing up](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#backing-up-gitlab) and [upgrading](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#upgrading-gitlab) GitLab.

## Related services

- [Forgejo](forgejo.md) — Software forge (Git hosting service, etc.)
- [Gitea](gitea.md) — Software forge (Git hosting service, etc.)
- [Radicle node](radicle-node.md) — Network daemon for the [Radicle](https://radicle.dev/) network, a peer-to-peer code collaboration stack built on Git
