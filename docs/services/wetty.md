<!--
SPDX-FileCopyrightText: 2023-2025 MASH project contributors
SPDX-FileCopyrightText: 2023-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Wetty

The playbook can install and configure [Wetty](https://github.com/butlerx/wetty) for you.

Wetty is an SSH terminal over HTTP/HTTPS, useful for when on a strict network which disallows outbound SSH traffic, or when only a browser can be used (like a managed chromebook).

See the project's [documentation](https://butlerx.github.io/wetty) to learn what Wetty does and why it might be useful to you.

For details about configuring the [Ansible role for Wetty](https://github.com/mother-of-all-self-hosting/ansible-role-wetty), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-wetty/blob/main/docs/configuring-wetty.md) online
- 📁 `roles/galaxy/wetty/docs/configuring-wetty.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# wetty                                                                #
#                                                                      #
########################################################################

wetty_enabled: true
wetty_hostname: mash.example.com
wetty_path_prefix: /wetty

wetty_environment_variables_ssh_host: example.com

########################################################################
#                                                                      #
# /wetty                                                               #
#                                                                      #
########################################################################
```

### Configure SSH port for Wetty (optional)

By default Wetty is configured to connect to the port 22 of the SSH server. If you wish to have the instance connect to another port, add the following configuration to your `vars.yml` file and adjust the port as you see fit.

```yaml
wetty_environment_variables_ssh_port: 222
```

## Usage

After running the command for installation, the Wetty instance becomes available at the URL specified with `wetty_hostname` and `wetty_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/wetty` and connects to `example.com` on port `22`.

Once connected, you can log in with SSH with the username and password.

>[!NOTE]
> Wetty only supports password authentication, so if the SSH daemon at `wetty_environment_variables_ssh_host` only allows pubkey authentication you will not be able to connect.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-wetty/blob/main/docs/configuring-wetty.md#troubleshooting) on the role's documentation for details.

## Related services

- [Termix](termix.md) — Server management platform with SSH terminal
