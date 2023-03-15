# Configuring the Ansible playbook

To configure the playbook, you need to have done the following things:

- have a server where services will run
- [retrieved the playbook's source code](getting-the-playbook.md) to your computer

You can then follow these steps inside the playbook directory:

1. create a directory to hold your configuration (`mkdir inventory/host_vars/<your-domain>`)

2. copy the sample configuration file (`cp examples/vars.yml inventory/host_vars/<your-domain>/vars.yml`)

3. edit the configuration file (`inventory/host_vars/<your-domain>/vars.yml`) to your liking. You should [enable one or more services](services/README.md) in your `vars.yml` file. You may also take a look at the various `roles/**/ROLE_NAME_HERE/defaults/main.yml` files and see if there's something you'd like to copy over and override in your `vars.yml` configuration file.

4. copy the sample inventory hosts file (`cp examples/hosts inventory/hosts`)

5. edit the inventory hosts file (`inventory/hosts`) to your liking

When you're done with all the configuration you'd like to do, continue with [Installing](installing.md).
