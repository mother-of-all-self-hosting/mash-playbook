<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ArtiDezi orchestrator

The playbook can install and configure the orchestrator of [ArtiDezi](https://github.com/devture/artidezi) for you.

ArtiDezi is a self-hosted tool which lets coding agents do routine maintenance on your repositories. The orchestrator is its trusted side: it holds the forge credentials, hands out work and judges the results. The agents run on [workers](../artidezi_worker/README.md), usually on other machines.

For details about configuring the [Ansible role for the ArtiDezi orchestrator](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md) online
- 📁 `roles/galaxy/artidezi_orchestrator/docs/configuring-artidezi-orchestrator.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server (or another reverse proxy; refer to the role's documentation)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# artidezi-orchestrator                                                #
#                                                                      #
########################################################################

artidezi_orchestrator_enabled: true

artidezi_orchestrator_hostname: artidezi.example.com

artidezi_orchestrator_secrets:
  admin-token: "{{ vault_artidezi_orchestrator_admin_token }}"

# Forges, workers, agent profiles and projects. Refer to the role's documentation.
artidezi_orchestrator_configuration_extension_yaml: |
  instance:
    bot_identity:
      name: ArtiDezi
      email: artidezi@example.com

########################################################################
#                                                                      #
# /artidezi-orchestrator                                               #
#                                                                      #
########################################################################
```

## Running several instances

Each instance is an inventory host of its own. Refer to [Running multiple instances](../../docs/running-multiple-instances.md).

## Usage

After installation, workers connect to `https://artidezi.example.com`. To add one, list it in the orchestrator's configuration and set up the [worker](../artidezi_worker/README.md).
