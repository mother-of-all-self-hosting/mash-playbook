<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Distribution Registry

The playbook can install and configure [Distribution Registry](https://github.com/distribution/distribution/) for you.

Distribution Registry is a stateless, scalable server side application that stores and lets you distribute container images and other content.

See the project's [documentation](https://distribution.github.io/distribution/) to learn what Distribution Registry does and why it might be useful to you.

For details about configuring the [Ansible role for Distribution Registry](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry/blob/main/docs/configuring-distribution-registry.md) online
- 📁 `roles/galaxy/anki/docs/configuring-distribution-registry.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> This playbook supports installing a container image registry which is:
>
> - completely public, when it comes to pulling images
> - IP-restricted, when it comes to pushing images
>
> Authentication is not supported.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# docker_registry                                                      #
#                                                                      #
########################################################################

docker_registry_enabled: true

docker_registry_hostname: registry.example.com

########################################################################
#                                                                      #
# /docker_registry                                                     #
#                                                                      #
########################################################################
```

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry/blob/main/docs/configuring-distribution-registry.md#adjusting-the-playbook-configuration) on the role's documentation for other settings, such as whitelisting IPs.

## Usage

After running the command for installation, the Distribution Registry instance becomes available at the URL specified with `docker_registry_hostname`. With the configuration above, the service is hosted at `https://registry.example.com`.

>[!NOTE]
> The base URL (e.g. `https://registry.example.com`) serves an empty (blank) page. To browse your registry's images via a web interface, you may need another piece of software, like [Docker Registry Browser](docker-registry-browser.md).

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry/blob/main/docs/configuring-distribution-registry.md#usage) on the role's documentation for details.

## Related services

- [Docker Registry Browser](docker-registry-browser.md) — Web Interface for the Docker Registry HTTP API V2 written in Ruby on Rails
- [Docker Registry Purger](docker-registry-purger.md) — a small tool used for purging a private Docker Registry's old tags
