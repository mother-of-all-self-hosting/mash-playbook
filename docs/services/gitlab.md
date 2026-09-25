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
- (optional) [Postgres](postgres.md) database — required on the default configuration
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

If [Postgres](postgres.md) and [exim-relay](exim-relay.md) are enabled on the playbook, GitLab is wired to them automatically.

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
