<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Syncthing

The playbook can install and configure [Syncthing](https://syncthing.net/) for you.

Syncthing is a continuous file synchronization program which synchronizes files between two or more computers in real time, safely protected from prying eyes.

See the project's [documentation](https://docs.syncthing.net/) to learn what Syncthing does and why it might be useful to you.

For details about configuring the [Ansible role for Syncthing](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing/blob/main/docs/configuring-syncthing.md) online
- 📁 `roles/galaxy/syncthing/docs/configuring-syncthing.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

syncthing_enabled: true

syncthing_hostname: mash.example.com
syncthing_path_prefix: /syncthing

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

For Syncthing, it is configured to enable the HTTP Basic authentication on Traefik by default. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing/blob/main/docs/configuring-syncthing.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up.

## Usage

After running the command for installation, the Syncthing instance becomes available at the URL specified with `syncthing_hostname` and `syncthing_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/syncthing`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing/blob/main/docs/configuring-syncthing.md#usage) on the role's documentation for details about usage, including recommended settings.
