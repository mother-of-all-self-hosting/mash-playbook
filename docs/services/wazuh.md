<!--
SPDX-FileCopyrightText: 2025, 2026 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Wazuh

The playbook can install and configure [Wazuh](https://wazuh.com/) for you.

Wazuh is an open source security platform providing unified SIEM, threat detection, and compliance monitoring. It runs as three containers: a manager (rules engine and agent coordinator), an indexer (OpenSearch-based event storage), and a dashboard (web UI).

See the project's [documentation](https://documentation.wazuh.com/current/index.html) to learn what Wazuh does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Prerequisites

Deploying Wazuh requires two additional Ansible collections:

- [community.general](https://github.com/ansible-collections/community.general) — for XML configuration file management
- [ansible.posix](https://github.com/ansible-collections/ansible.posix) — for setting `vm.max_map_count` (required by OpenSearch)

Install them via:

```sh
ansible-galaxy collection install community.general ansible.posix
```

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# wazuh                                                                #
#                                                                      #
########################################################################

wazuh_enabled: true

wazuh_hostname: wazuh.example.com

# Generate with: pwgen -s 63 3 (add at least one special character to each)
wazuh_indexer_admin_password: ""
wazuh_indexer_kibanaserver_password: ""
wazuh_manager_api_password: ""

# Generate with: pwgen -s 22 2 (must be exactly 22 characters)
wazuh_indexer_admin_password_salt: ""
wazuh_indexer_kibanaserver_password_salt: ""

########################################################################
#                                                                      #
# /wazuh                                                               #
#                                                                      #
########################################################################
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- The [Wazuh role](https://github.com/spatterIight/ansible-role-wazuh/)'s [`defaults/main.yml`](https://github.com/spatterIight/ansible-role-wazuh/blob/main/defaults/main.yml) for additional variables that you can customize via your `vars.yml` file.
- The [Wazuh role documentation](https://github.com/spatterIight/ansible-role-wazuh/blob/main/docs/configuring-wazuh.md#usage).

## Usage

After running the installation command, the Wazuh dashboard becomes available at the URL specified with `wazuh_hostname`. With the configuration above, the service is hosted at `https://wazuh.example.com`.

To get started, open the URL with a web browser to log in to the instance with the username `admin` and the password set to `wazuh_indexer_admin_password`.
