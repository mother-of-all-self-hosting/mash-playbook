<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Ollama

The playbook can install and configure [Ollama](https://ollama.com/) for you.

Ollama is a server for running large language models on your own hardware.

See the project's [documentation](https://docs.ollama.com/) to learn what Ollama does and why it might be useful to you.

For details about configuring the [Ansible role for Ollama](https://github.com/mother-of-all-self-hosting/ansible-role-ollama), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-ollama/blob/main/docs/configuring-ollama.md) online
- 📁 `roles/galaxy/ollama/docs/configuring-ollama.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](../traefik/README.md) — Reverse-proxy server for exposing Ollama publicly

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# ollama                                                               #
#                                                                      #
########################################################################

ollama_enabled: true

########################################################################
#                                                                      #
# /ollama                                                              #
#                                                                      #
########################################################################
```

If you enable Ollama before [Open WebUI](../open_webui/README.md) starts for the first time, the playbook automatically configures Open WebUI to connect to it by default. If Open WebUI has already started, add the connection in its admin panel; see [Connecting to models](../open_webui/README.md#connecting-to-models) for details.

### Expose the instance publicly (optional)

By default, the Ollama instance is not exposed externally, as it is mainly intended to be used in the internal network.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which Ollama is served.
ollama_hostname: "ollama.example.com"
```

>[!WARNING]
> Ollama's API has no authentication, so anyone who can reach it can use your models and download new ones. If you expose it, consider protecting it with HTTP Basic Authentication (see `ollama_container_labels_traefik_middleware_basic_auth_*` on the role's [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-ollama/blob/main/defaults/main.yml)).

### Enable hardware acceleration (optional)

By default, Ollama runs models on the CPU. To run them on a GPU, refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ollama/blob/main/docs/configuring-ollama.md#enable-hardware-acceleration-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Ollama instance becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the URL specified with `ollama_hostname`. With the configuration above, the service is hosted at `https://ollama.example.com`.

Ollama does not come with any models. To download one, run the command below on the server:

```sh
docker exec -it mash-ollama ollama pull llama3.2
```

See the [model library](https://ollama.com/library) for the models which are available.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ollama/blob/main/docs/configuring-ollama.md#troubleshooting) on the role's documentation for details.

## Related services

- [Open WebUI](../open_webui/README.md) — Self-hosted web interface for AI models
