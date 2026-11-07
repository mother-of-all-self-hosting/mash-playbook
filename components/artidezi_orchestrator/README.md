<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ArtiDezi orchestrator

The playbook can install and configure the orchestrator of [ArtiDezi](https://github.com/devture/artidezi) for you.

ArtiDezi is a self-hosted maintenance agent that pushes the boring buttons: it lets coding agents do routine maintenance on your repositories, without giving them your forge credentials. The orchestrator is its trusted part: it holds the forge credentials, hands out work and publishes the results. The agents run on [workers](../artidezi_worker/README.md), on other machines.

See the project's [documentation](https://github.com/devture/artidezi/blob/main/docs/README.md) to learn what ArtiDezi does and why it might be useful to you.

For details about configuring the [Ansible role for the ArtiDezi orchestrator](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md) online
- 📁 `roles/galaxy/artidezi_orchestrator/docs/configuring-artidezi-orchestrator.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server
- one or more [ArtiDezi workers](../artidezi_worker/README.md), usually on other servers

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# artidezi_orchestrator                                                #
#                                                                      #
########################################################################

artidezi_orchestrator_enabled: true

artidezi_orchestrator_hostname: artidezi.example.com

########################################################################
#                                                                      #
# /artidezi_orchestrator                                               #
#                                                                      #
########################################################################
```

### Set the ArtiDezi configuration and secrets

The orchestrator also needs its ArtiDezi configuration (the forges, worker pools, agent profiles and projects) in `artidezi_orchestrator_configuration_extension_yaml`, and the credentials it refers to in `artidezi_orchestrator_secrets`. The playbook refuses to install it without them. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md#set-the-artidezi-configuration) and [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md#set-the-secrets) on the role's documentation for details.

### Enabling the web UI (optional)

The web UI is off by default. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md#enabling-the-web-ui-optional) on the role's documentation for details.

### Checking GitHub App access before installing (optional)

For GitHub forges, the role can verify the App's access to the configured repositories before installing a configuration. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md#checking-github-app-access-before-installing-optional) on the role's documentation for details.

### Running several instances (optional)

Each instance is an inventory host of its own. Refer to [Running multiple instances](../../docs/running-multiple-instances.md), and to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md#running-several-instances-optional) on the role's documentation for what has to differ between instances.

## Usage

After running the command for installation, the orchestrator becomes available at the URL specified with `artidezi_orchestrator_hostname`. With the configuration above, the service is hosted at `https://artidezi.example.com`.

Workers connect to that URL. To add one, list it in the orchestrator's configuration and set up the [worker](../artidezi_worker/README.md).

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md#usage) on the role's documentation for details about the usage, backups and upgrades.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-artidezi-orchestrator/blob/main/docs/configuring-artidezi-orchestrator.md#troubleshooting) on the role's documentation for details.

## Related services

- [ArtiDezi worker](../artidezi_worker/README.md) - Runs coding agents for an ArtiDezi orchestrator
- [Forgejo](../forgejo/README.md) - Software forge (Git hosting service, etc.), one of the forges ArtiDezi works with
