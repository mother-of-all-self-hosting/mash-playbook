<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Matrix Rooms Search API

The playbook can install and configure [Matrix Rooms Search](https://github.com/etkecc/mrs) for you.

Matrix Rooms Search is a fully-featured, standalone, [Matrix](https://matrix.org/) rooms search service.

See the project's [documentation](https://github.com/etkecc/mrs/blob/main/README.md) to learn what Matrix Rooms Search does and why it might be useful to you.

For details about configuring the [Ansible role for Matrix Rooms Search](https://github.com/mother-of-all-self-hosting/ansible-role-mrs), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-mrs/blob/main/docs/configuring-mrs.md) online
- 📁 `roles/galaxy/mrs/docs/configuring-mrs.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# mrs                                                                  #
#                                                                      #
########################################################################

mrs_enabled: true

mrs_hostname: mrs.example.com

########################################################################
#                                                                      #
# /mrs                                                                 #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mrs/blob/main/docs/configuring-mrs.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings.

## Usage

After running the command for installation, the Matrix Rooms Search instance becomes available at the URL specified with `mrs_hostname`. With the configuration above, the service is hosted at `https://mrs.example.com`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mrs/blob/main/docs/configuring-mrs.md#usage) on the role's documentation for details about the usage.

## Related services

- [Cinny](../cinny/README.md) — Elegant web client for Matrix
