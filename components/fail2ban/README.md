<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 aine-etke
SPDX-FileCopyrightText: 2025-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Fail2Ban

The playbook can install and configure [Fail2Ban](https://github.com/fail2ban/fail2ban/wiki) for you.

For details about configuring the role, you can check them via:

- 🌐 [the role's `defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-fail2ban/blob/main/defaults/main.yml) online
- 📁 `roles/galaxy/fail2ban/defaults/main.yml` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

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

## Related services

Refer to [this section](../../docs/supported-services.md#system-related-components) for other system-related services.
