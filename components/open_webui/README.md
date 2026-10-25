<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Open WebUI

The playbook can install and configure [Open WebUI](https://openwebui.com/) for you.

Open WebUI is a self-hosted web interface for AI models, which works with [Ollama](../ollama/README.md) and OpenAI-compatible APIs.

See the project's [documentation](https://docs.openwebui.com/) to learn what Open WebUI does and why it might be useful to you.

For details about configuring the [Ansible role for Open WebUI](https://github.com/mother-of-all-self-hosting/ansible-role-open-webui), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-open-webui/blob/main/docs/configuring-open-webui.md) online
- 📁 `roles/galaxy/open_webui/docs/configuring-open-webui.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](../traefik/README.md) reverse-proxy server
- (optional) [Ollama](../ollama/README.md) server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# open_webui                                                           #
#                                                                      #
########################################################################

open_webui_enabled: true

open_webui_hostname: open-webui.example.com

########################################################################
#                                                                      #
# /open_webui                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting Open WebUI under a subpath (by configuring the `open_webui_path_prefix` variable) is not possible due to Open WebUI's technical limitations.

### Select database to use

Open WebUI can use either Postgres or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-open-webui/blob/main/docs/configuring-open-webui.md#specify-database) on the role's documentation for details.

### Set administrator's account details (optional)

By default, the first user who signs up becomes the administrator, so anyone who reaches the instance before you can take that role. To have Open WebUI create the administrator's account on its first start instead, refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-open-webui/blob/main/docs/configuring-open-webui.md#set-the-administrators-account-details-optional) on the role's documentation.

### Connecting to models

If you enable the [Ollama](../ollama/README.md) service in your inventory configuration before Open WebUI starts for the first time, the playbook automatically configures Open WebUI to connect to it by default.

By default, Open WebUI reads its connections from the environment only on its first start, and keeps them in its database afterwards. If you enable Ollama after Open WebUI has started for the first time, add the connection in the admin panel. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-open-webui/blob/main/docs/configuring-open-webui.md#connecting-to-models) on the role's documentation for details, including how to connect to an OpenAI-compatible API or disable persistent configuration so that inventory changes take effect on subsequent starts.

## Usage

After running the command for installation, the Open WebUI instance becomes available at the URL specified with `open_webui_hostname`. With the configuration above, the service is hosted at `https://open-webui.example.com`.

To get started, open the URL with a web browser, and create a user or log in with the administrator's account set above. The first user becomes the administrator, and Open WebUI then turns sign-up off. To let other users sign up, turn it on again in the admin panel.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-open-webui/blob/main/docs/configuring-open-webui.md#troubleshooting) on the role's documentation for details.

## Related services

- [Ollama](../ollama/README.md) — Server for running large language models on your own hardware
