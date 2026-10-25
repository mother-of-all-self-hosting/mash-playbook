<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Fail2ban

To enable [fail2ban](https://fail2ban.org/wiki/index.php/Main_Page) installation, management and integration with SSHd, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# system                                                               #
#                                                                      #
########################################################################

system_security_fail2ban_enabled: true

system_security_fail2ban_sshd_port: 22
# If you enabled playbook-managed SSH as well (see its documentation),
# you can replace the line above with the following:
# system_security_fail2ban_sshd_port: "{{ system_security_ssh_port }}"

########################################################################
#                                                                      #
# /system                                                              #
#                                                                      #
########################################################################
```
