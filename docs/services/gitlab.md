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
- (optional) [Postgres](postgres.md) database — used instead of the database server bundled in the GitLab container image, if enabled
- (optional) [Valkey](valkey.md) data-store — used instead of the Redis server bundled in the GitLab container image, if enabled
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

If [Postgres](postgres.md), [Valkey](valkey.md) and [exim-relay](exim-relay.md) are enabled on the playbook, GitLab is wired to them automatically. Otherwise, GitLab uses the Postgres and Redis servers bundled in its container image.

>[!NOTE]
> Switching between the bundled and the playbook's Postgres server (e.g. by enabling Postgres after GitLab has been installed) does not migrate any data, and GitLab starts with an empty database. Decide on it before installing GitLab, or [back up](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#backing-up-gitlab) the instance and restore the backup after switching.

### Configure the database and Valkey

With Postgres enabled, the playbook creates a database for GitLab on it. GitLab requires a Postgres extension which it cannot create on its own, and some changes to the settings of the Postgres server. Refer to [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#using-an-external-postgres-server) on the role's documentation for details.

With Valkey enabled, GitLab uses the shared Valkey instance (`mash-valkey`). As described on the [documentation for configuring Valkey](valkey.md), sharing a Valkey instance among several services is not recommended. If other services use Valkey as well, consider setting up a Valkey instance dedicated to GitLab, by following [the instructions for NetBox](netbox.md#setting-up-a-dedicated-valkey-instance) (adjusting `netbox` to `gitlab`), and pointing GitLab to it with the following configuration:

```yaml
gitlab_redis_hostname: mash-gitlab-valkey

gitlab_container_additional_networks_custom:
  - mash-gitlab-valkey

gitlab_systemd_required_services_list_custom:
  - mash-gitlab-valkey.service
```

To keep using the servers bundled in the GitLab container image even though Postgres or Valkey is enabled on the playbook, add the following configuration to your `vars.yml` file:

```yaml
# Use the bundled Postgres server
gitlab_database_type: bundled

# Use the bundled Redis server
gitlab_redis_hostname: ''
```

Refer to [this section](https://github.com/spatterIight/ansible-role-gitlab/blob/main/docs/configuring-gitlab.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings such as setting the password for the `root` user, enabling Git over SSH, and enabling the container registry.

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
