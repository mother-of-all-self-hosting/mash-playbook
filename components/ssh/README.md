<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 aine-etke
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# SSH server

> [!WARNING]
> Advanced functionality! While the default config with a few adjustments was battle tested on hundreds of servers, you should use it with caution and verify everything before you apply the changes!

To enable [ssh server](https://www.openssh.com/) config and authorized/unauthorized keys management, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

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

The [default configuration](https://github.com/mother-of-all-self-hosting/ansible-role-ssh/blob/main/defaults/main.yml) is good enough as-is, but we strongly suggest you to **verify everything before applying any changes!**, otherwise you may lock yourself out of the server.

With this configuration, the default `/etc/ssh/sshd_config` file on your server will be replaced by a new one, managed by the [ssh role](https://github.com/mother-of-all-self-hosting/ansible-role-ssh) (see its [templates/etc/ssh/sshd_config.j2](https://github.com/mother-of-all-self-hosting/ansible-role-ssh/blob/main/templates/etc/ssh/sshd_config.j2) file).

There are various configuration options — check the defaults and adjust them to your needs.
