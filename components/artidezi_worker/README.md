<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ArtiDezi worker

The playbook can install and configure a worker of [ArtiDezi](https://github.com/devture/artidezi) for you.

ArtiDezi is a self-hosted maintenance agent that pushes the boring buttons: it lets coding agents do routine maintenance on your repositories, without giving them your forge credentials. A worker runs the coding agents on tasks handed out by an [ArtiDezi orchestrator](../artidezi_orchestrator/README.md).

See the project's [documentation](https://github.com/devture/artidezi/blob/main/docs/README.md) to learn what ArtiDezi does and why it might be useful to you.

>[!WARNING]
> A worker is not a sandbox. It runs repository code and a coding agent, which can read the harness credentials stored on it. Give each worker an expendable server of its own, with nothing else on it.

For details about configuring the [Ansible role for the ArtiDezi worker](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker/blob/main/docs/configuring-artidezi-worker.md) online
- 📁 `roles/galaxy/artidezi_worker/docs/configuring-artidezi-worker.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- an [ArtiDezi orchestrator](../artidezi_orchestrator/README.md), usually on another server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# artidezi_worker                                                      #
#                                                                      #
########################################################################

artidezi_worker_enabled: true

artidezi_worker_orchestrator_url: https://artidezi.example.com
artidezi_worker_pool: maintenance
artidezi_worker_id: worker-1
artidezi_worker_token: WORKER_TOKEN_HERE

########################################################################
#                                                                      #
# /artidezi_worker                                                     #
#                                                                      #
########################################################################
```

The pool, the id and the token have to match what the orchestrator's configuration lists for this worker.

### Choose a harness

A worker needs at least 1 coding-agent harness. To offer Codex, add the following configuration to your `vars.yml` file:

```yaml
artidezi_worker_codex_enabled: true
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker/blob/main/docs/configuring-artidezi-worker.md#choose-a-harness) on the role's documentation for Pi and the harness versions.

### Adding project tooling (optional)

The worker's image bundles little besides the harness. Tools from [mise](https://mise.jdx.dev/), apt packages and your own Dockerfile steps can be added to it. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker/blob/main/docs/configuring-artidezi-worker.md#adding-project-tooling-optional) on the role's documentation for details.

### Running on the host instead of in a container (optional)

By default, the worker and its tasks run in a hardened container. For tasks which need more privilege, such as Docker, the worker can run on the host instead. In that mode, the role installs no harness or tooling, and the worker needs a user of its own (not the playbook's `mash_playbook_uid`), with `artidezi_worker_base_path` outside of `/mash`. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker/blob/main/docs/configuring-artidezi-worker.md#running-on-the-host-instead-of-in-a-container-optional) on the role's documentation for details.

## Usage

After running the command for installation, the worker connects to the orchestrator and appears on its Workers page.

Before it can run a job, provide the credentials of the model endpoint on the worker. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker/blob/main/docs/configuring-artidezi-worker.md#providing-the-harness-credentials) on the role's documentation for details.

Re-running the playbook restarts the worker when its configuration or image changed, which stops the attempt it is running. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker/blob/main/docs/configuring-artidezi-worker.md#upgrading-and-restarting) on the role's documentation for details.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker/blob/main/docs/configuring-artidezi-worker.md#troubleshooting) on the role's documentation for details.

## Related services

- [ArtiDezi orchestrator](../artidezi_orchestrator/README.md) - The trusted server of ArtiDezi, which hands out work to workers
