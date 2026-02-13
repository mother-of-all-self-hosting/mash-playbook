<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Yggstack

The playbook can install and configure [Yggstack](https://github.com/yggdrasil-network/yggstack) for you.

Yggstack is a SOCKS5 proxy server and TCP port forwarder for [Yggdrasil](https://yggdrasil-network.github.io), an early-stage implementation of a fully end-to-end encrypted IPv6 network.

See the project's [documentation](https://github.com/yggdrasil-network/yggstack/blob/develop/README.md) to learn what Yggstack does and why it might be useful to you.

For details about configuring the [Ansible role for Yggstack](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2BzsfYJzpSCK4tC8kCR1uCooZYX5), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2BzsfYJzpSCK4tC8kCR1uCooZYX5/tree/docs/configuring-yggstack.md) online
- 📁 `roles/galaxy/yggstack/docs/configuring-yggstack.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# yggstack                                                             #
#                                                                      #
########################################################################

yggstack_enabled: true

########################################################################
#                                                                      #
# /yggstack                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, Yggstack becomes available at the IPv6 address which the service generates for you. The IPv6 address, its subnet, and your public key have been been logged to the console logs on the startup. The configuration file (`yggdrasil.conf`) can be found in `yggstack_data_path`.

Refer to [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2BzsfYJzpSCK4tC8kCR1uCooZYX5/tree/docs/configuring-yggstack.md#usage) for details about how to set up Yggstack.

### Connecting with Traefik

By placing Yggstack before Traefik, it will be possible to serve multiple services via Yggstack. Please follow the example below:

```yaml
# Expose Traefik to Yggdrasil at port 80 and 443
yggstack_process_extra_arguments_custom:
  - -remote-tcp 80:TRAEFIK_INTERNAL_IP_HERE:8080
  - -remote-tcp 443:TRAEFIK_INTERNAL_IP_HERE:8443

# Connect Yggstack with Traefik
traefik_container_additional_networks_custom:
  - "{{ yggstack_container_network }}"

# Unset the port 80 which Traefik opens to the internet
traefik_container_web_host_bind_port: null

# Unset the port 443 which Traefik opens to the internet
traefik_container_web_secure_host_bind_port: null

# Disable the web entrypoint from being redirected to web-secure
traefik_config_entrypoint_web_to_web_secure_redirection_enabled: false
```

To expose a service via Traefik, add the configuration like below to your `vars.yml` file:

>[!NOTE]
> This setup requires the connection to the internet to resolve the hostname, if you do not prepare another solution by yourself.

```yaml
YOUR-SERVICE_enabled: true

YOUR-SERVICE_hostname: SET_HOSTNAME_HERE

# Set the scheme to HTTP. Since Yggdrasil Network is end-to-end encrypted by default, you can ignore the message about insecure connection.
YOUR-SERVICE_scheme: http

# Override the default entrypoint (web-secure)
YOUR-SERVICE_container_labels_traefik_entrypoints: web
```

If the service requires a TLS certificate for some reason, you can have Traefik obtain one for the hostname by setting it to `traefik_additional_domains_to_obtain_certificates_for_custom`. Note because by default it requires connection to the internet as it utilizes Let's Encrypt as the ACME certificate resolver, you might have to restart Traefik before enabling Yggstack.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2BzsfYJzpSCK4tC8kCR1uCooZYX5/tree/docs/configuring-yggstack.md#troubleshooting) on the role's documentation for details.

## References

- <https://yggdrasil-network.github.io/about.html> — Basic concepts about Yggdrasil Network
- <https://yggdrasil-network.github.io/services.html>
