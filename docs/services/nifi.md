<!--
SPDX-FileCopyrightText: 2025 spatterlight
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Apache NiFi

The playbook can install and configure [Apache NiFi](https://nifi.apache.org/) for you.

Apache NiFi is an open-source, easy to use, powerful, and reliable system to process and distribute data.

See the project's [documentation](https://nifi.apache.org/components/) to learn what Apache NiFi does and why it might be useful to you.

For details about configuring the [Ansible role for Apache NiFi](https://github.com/spatterIight/ansible-role-nifi), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-nifi/blob/main/docs/configuring-nifi.md) online
- 📁 `roles/galaxy/nifi/docs/configuring-nifi.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Prerequisites

To deploy Apache NiFi using this role it is necessary that:

1. The [community.general](https://github.com/ansible-collections/community.general) collection be installed. This is needed to support modifying XML configuration files.
2. The [community.crypto](https://github.com/ansible-collections/community.crypto) collection be installed. This is needed to create the self-signed HTTPS certificate for Apache NiFi.
3. The `keytool` program be available on the target host. This can be installed via `apt install default-jre` on Debian systems.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# nifi                                                                 #
#                                                                      #
########################################################################

nifi_enabled: true

nifi_hostname: nifi.example.com

########################################################################
#                                                                      #
# /nifi                                                                #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/spatterIight/ansible-role-nifi/blob/main/docs/configuring-nifi.md#adjusting-the-playbook-configuration) on the role's documentation for details about what to be added.

To integrate with Traefik, the custom Traefik `serversTransports` definition is required since Apache NiFi only supports listening via HTTPS. Because this "backend" certificate is self-signed, Traefik must be configured to skip verifying it:

```yaml
########################################################################
#                                                                      #
# traefik                                                              #
#                                                                      #
########################################################################

# Other Traefik configuration …

traefik_provider_configuration_extension_yaml: |
  http:
    serversTransports:
      {{ nifi_traefik_serverstransport }}:
        insecureSkipVerify: true

########################################################################
#                                                                      #
# /traefik                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Apache NiFi instance becomes available at the specified hostname like `https://nifi.example.com`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-nifi/blob/main/docs/configuring-nifi.md#usage) on the role's documentation for details about how to use the service.

## Troubleshooting

Refer to [this section](https://github.com/spatterIight/ansible-role-nifi/blob/main/docs/configuring-nifi.md#troubleshooting) on the role's documentation for details.
