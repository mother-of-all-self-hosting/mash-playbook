<!--
SPDX-FileCopyrightText: 2025 - 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Apache NiFi Registry

The playbook can install and configure [Apache NiFi Registry](https://nifi.apache.org/projects/registry/) for you.

Apache NiFi Registry is a complementary application for [Apache NiFi](nifi.md) that provides a central location for storing and managing versioned flows (and extension bundles) shared across one or more Apache NiFi instances.

See the project's [documentation](https://nifi.apache.org/docs/nifi-registry-docs/) to learn what Apache NiFi Registry does and why it might be useful to you.

For details about configuring the [Ansible role for Apache NiFi Registry](https://github.com/spatterIight/ansible-role-nifi-registry), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-nifi-registry/blob/main/docs/configuring-nifi-registry.md) online
- 📁 `roles/galaxy/nifi_registry/docs/configuring-nifi-registry.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# nifi-registry                                                        #
#                                                                      #
########################################################################

nifi_registry_enabled: true

nifi_registry_hostname: nifi-registry.example.com

# The credentials Traefik asks for before letting a request through to Apache NiFi Registry.
# Generate a password using `pwgen -s 32 1`, or some other way
nifi_registry_basic_auth_username: admin
nifi_registry_basic_auth_password: ""

########################################################################
#                                                                      #
# /nifi-registry                                                       #
#                                                                      #
########################################################################
```

Apache NiFi Registry has no login of its own, so the role protects it with HTTP basic authentication on Traefik. See [this section](https://github.com/spatterIight/ansible-role-nifi-registry/blob/main/docs/configuring-nifi-registry.md#how-this-role-secures-apache-nifi-registry) on the role's documentation for details.

### Connecting Apache NiFi

If [Apache NiFi](nifi.md) is enabled on the same server, the playbook automatically attaches it to the Apache NiFi Registry container network, so no additional network configuration is needed.

In Apache NiFi, open **Controller Settings** → **Registry Clients**, add a **NifiRegistryFlowRegistryClient**, and set its **URL** to `http://mash-nifi-registry:18080` (the value of `nifi_registry_identifier`, followed by port `18080`).

## Usage

After running the command for installation, the Apache NiFi Registry instance becomes available at the URL specified with `nifi_registry_hostname`. With the configuration above, the service is hosted at `https://nifi-registry.example.com`. Log in with the basic authentication credentials you configured.

## Troubleshooting

See [this section](https://github.com/spatterIight/ansible-role-nifi-registry/blob/main/docs/configuring-nifi-registry.md#troubleshooting) on the role's documentation for details.

## Related services

- [Apache NiFi](nifi.md) — An easy to use, powerful, and reliable system to process and distribute data
