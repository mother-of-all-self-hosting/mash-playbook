<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ArtiDezi worker

The playbook can install and configure a worker of [ArtiDezi](https://github.com/devture/artidezi) for you.

A worker runs coding agents on tasks handed out by an [ArtiDezi orchestrator](../artidezi_orchestrator/README.md). It's not a sandbox: an agent can read the harness credentials on its worker, so give each worker an expendable machine of its own.

For details about configuring the [Ansible role for the ArtiDezi worker](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-worker/blob/main/docs/configuring-artidezi-worker.md) online
- 📁 `roles/galaxy/artidezi_worker/docs/configuring-artidezi-worker.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# artidezi-worker                                                      #
#                                                                      #
########################################################################

artidezi_worker_enabled: true

artidezi_worker_orchestrator_url: https://artidezi.example.com
artidezi_worker_pool: maintenance
artidezi_worker_id: worker-1
artidezi_worker_token: "{{ vault_artidezi_worker_token }}"

artidezi_worker_codex_enabled: true

########################################################################
#                                                                      #
# /artidezi-worker                                                     #
#                                                                      #
########################################################################
```

Harnesses and project tooling (`mise`, packages, Dockerfile additions) are also configured through the role. Refer to its documentation.
