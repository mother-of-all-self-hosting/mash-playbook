# Soft Serve

This playbook can configure [Soft Serve](https://github.com/charmbracelet/soft-serve).

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
# It will be used for generating git clone URLs (e.g. ssh://mash.example.com/repository.git)
soft_serve_hostname: mash.example.com
soft_serve_container_bind_port: 2222 # Expose Soft Serve's port. For git servers the usual git-over-ssh port is 22
soft_serve_initial_admin_key: YOUR PUBLIC SSH KEY HERE # This key will be able to authenticate with ANY user until you configure Soft Serve

########################################################################
#                                                                      #
# /soft-serve                                                          #
#                                                                      #
########################################################################
```

## Usage

After you've installed Soft Serve, you can `ssh your-user@mash.example.com -p 2222` with the ssh key you defined in `soft_serve_initial_admin_key` to see TUI and follow the instructions to configure Soft Serve further.

Note that you have to [finish the configuration yourself](https://github.com/charmbracelet/soft-serve#configuration), otherwise any user with `soft_serve_initial_admin_key` will work as admin.
