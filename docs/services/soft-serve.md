<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Soft Serve

[Soft Serve](https://github.com/charmbracelet/soft-serve) is a tasty, self-hostable [Git](https://git-scm.com/) server for the command line.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# soft-serve                                                           #
#                                                                      #
########################################################################

soft_serve_enabled: true

# The hostname of this system.
# It will be used for generating git clone URLs (e.g. ssh://soft-serve.example.com/repository.git)
soft_serve_hostname: soft-serve.example.com

# Expose Soft Serve's port. For git servers the usual git-over-ssh port is 22
soft_serve_container_bind_port: 2222

# This key will be able to authenticate with ANY user until you configure Soft Serve
soft_serve_initial_admin_key: YOUR PUBLIC SSH KEY HERE

########################################################################
#                                                                      #
# /soft-serve                                                          #
#                                                                      #
########################################################################
```

## Usage

After you've installed Soft Serve, you can `ssh your-user@soft-serve.example.com -p 2222` with the SSH key defined in `soft_serve_initial_admin_key` to see its [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface) and follow the instructions to configure Soft Serve further.

Note that you have to [finish the configuration yourself](https://github.com/charmbracelet/soft-serve#configuration), otherwise any user with `soft_serve_initial_admin_key` will work as an admin.
