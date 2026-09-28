<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Docker Registry Browser

The playbook can install and configure [Docker Registry Browser](https://github.com/klausmeyer/docker-registry-browser) for you.

Docker Registry Browser is a web interface for the Docker Registry HTTP API V2, written in Ruby on Rails.

See the project's [documentation](https://github.com/klausmeyer/docker-registry-browser/blob/master/README.md) to learn what Docker Registry Browser does and why it might be useful to you.

The [Ansible role for Docker Registry Browser](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry-browser) is developed and maintained by the MASH project. For details about configuring Docker Registry Browser, you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry-browser/blob/main/docs/configuring-docker-registry-browser.md) online
- 📁 `roles/galaxy/docker_registry_browser/docs/configuring-docker-registry-browser.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# docker_registry_browser                                              #
#                                                                      #
########################################################################

docker_registry_browser_enabled: true

# Hosting under a subpath (such as `/browser`) allows the browser to co-exist
# on the same hostname as a Distribution Registry instance (see `docker-registry.md`).
docker_registry_browser_hostname: registry.example.com
docker_registry_browser_path_prefix: /browser

########################################################################
#                                                                      #
# /docker_registry_browser                                             #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry-browser/blob/main/docs/configuring-docker-registry-browser.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings such as the one for configuring HTTP Basic authentication.

## Usage

After running the command for installation, the Docker Registry Browser instance becomes available at the URL specified with `docker_registry_browser_hostname` and `docker_registry_browser_path_prefix`. With the configuration above, the service is hosted at `https://registry.example.com/browser`.

## Related services

- [Distribution Registry](docker-registry.md) — Container image distribution registry
