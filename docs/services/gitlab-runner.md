<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# GitLab Runner

The playbook can install and configure [GitLab Runner](https://docs.gitlab.com/runner/) for you.

GitLab Runner runs the CI/CD jobs of a [GitLab](gitlab.md) instance. It is set up with the [Docker executor](https://docs.gitlab.com/runner/executors/docker/): every job runs in a container of its own. See the project's [documentation](https://docs.gitlab.com/runner/) to learn more.

For details about configuring the [Ansible role for GitLab Runner](https://github.com/mother-of-all-self-hosting/ansible-role-gitlab-runner), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gitlab-runner/blob/main/docs/configuring-gitlab-runner.md) online
- 📁 `roles/galaxy/gitlab_runner/docs/configuring-gitlab-runner.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!WARNING]
> GitLab Runner starts the containers of its jobs through the host's Docker socket, which is equivalent to `root` access on the host. Only let it run jobs you trust.

## Prerequisites

Create a runner in GitLab first (e.g. **Admin area** → **CI/CD** → **Runners** → **New instance runner**), and copy the runner authentication token (`glrt-…`) that GitLab shows for it. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gitlab-runner/blob/main/docs/configuring-gitlab-runner.md#prerequisites) on the role's documentation for details.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gitlab_runner                                                        #
#                                                                      #
########################################################################

gitlab_runner_enabled: true

gitlab_runner_config_gitlab_url: https://gitlab.example.com

gitlab_runner_runners:
  - name: docker
    token: YOUR_RUNNER_AUTHENTICATION_TOKEN_HERE

########################################################################
#                                                                      #
# /gitlab_runner                                                       #
#                                                                      #
########################################################################
```

If [GitLab](gitlab.md) is enabled on the same host, `gitlab_runner_config_gitlab_url` defaults to its URL.

See [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gitlab-runner/blob/main/docs/configuring-gitlab-runner.md#adjusting-the-playbook-configuration) for other settings, such as the number of concurrent jobs, additional runners and Docker-in-Docker.

## Usage

After installation, the runner shows up as online in GitLab's list of runners, and starts running jobs.

If it does not, check its logs with `journalctl -fu mash-gitlab-runner` on the server.

## Related services

- [Forgejo Runner](forgejo-runner.md) — Runner to use with Forgejo Actions
- [GitLab](gitlab.md) — Complete DevOps platform (Git hosting service, CI/CD, etc.)
- [Woodpecker CI](woodpecker-ci.md) — Extensible Continuous Integration (CI) engine
