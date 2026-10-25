<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Swap

To enable [swap](https://en.wikipedia.org/wiki/Memory_paging) management (also read more in the [Swap](https://wiki.archlinux.org/title/Swap) article in the [Arch Linux Wiki](https://wiki.archlinux.org/)), add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# system                                                               #
#                                                                      #
########################################################################

system_swap_enabled: true

########################################################################
#                                                                      #
# /system                                                              #
#                                                                      #
########################################################################
```

A swap file will be created in `/var/swap` (configured using the `system_swap_path` variable) and enabled in your `/etc/fstab` file.

By default, the swap file will have `1GB` size, but you can set the `system_swap_size` variable in megabytes, example (4gb):

```yaml
system_swap_size: 4096
```

> [!WARNING]
> Changing `system_swap_size` subsequently will not recreate the SWAP file with the new size. You will need to disable swap, re-run the playbook (to make it clean up), then enable it again with the new size.
