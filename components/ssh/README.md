<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 aine-etke
SPDX-FileCopyrightText: 2025-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# SSH server management

> [!WARNING]
> Advanced functionality! While the default config with a few adjustments was battle tested on hundreds of servers, you should use it with caution and verify everything before you apply the changes. **Otherwise you may lock yourself out of the server!**

The playbook incorporates the [ansible-role-ssh](https://github.com/mother-of-all-self-hosting/ansible-role-ssh) Ansible role. It helps you to manage **OpenSSH server (sshd)** configuration and **authorized / unauthorized SSH keys**.

For details about configuring the role, you can check them via:

- 🌐 [the role's `defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-ssh/blob/main/defaults/main.yml) online
- 📁 `roles/galaxy/ssh/defaults/main.yml` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable it, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# system                                                               #
#                                                                      #
########################################################################

system_security_ssh_enabled: true

system_security_ssh_port: 22

system_security_ssh_authorizedkeys_host: [] # list of authorized public keys
system_security_ssh_unauthorizedkeys_host: [] # list of unauthorized/revoked public keys

########################################################################
#                                                                      #
# /system                                                              #
#                                                                      #
########################################################################
```

With this configuration, the default `/etc/ssh/sshd_config` file on your server will be replaced by a new one (refer to its [templates/etc/ssh/sshd_config.j2](https://github.com/mother-of-all-self-hosting/ansible-role-ssh/blob/main/templates/etc/ssh/sshd_config.j2) file).

There are various configuration options — check the defaults and adjust them to your needs.

## Related services

Refer to [this section](../../docs/supported-services.md#system-related-components) for other system-related services.
