# System-related configuration

This Ansible playbook can install and configure various system-related things for you.
All the sections below relates to the host OS instead of docker containers.

### swap

To enable [swap](https://en.wikipedia.org/wiki/Memory_paging) management, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

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

By default, swap file size calculated using the following formula: `total RAM * 2 if total RAM <= 2GB, else - 1GB`,
if you want to set different swap file size, you can set the `system_swap_size` var in megabytes, example (4gb):

```yaml
system_swap_size: 4096
```
