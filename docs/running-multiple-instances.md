## Running multiple instances of the same service on the same host

The way this playbook is structured, each Ansible role can only be invoked once and made to install one instance of the service it's responsible for.

If you need multiple instances (of whichever service), you'll need some workarounds as described below.

The example below focuses on hosting multiple [Valkey](services/valkey.md) instances, but you can apply it to hosting multiple instances or whole stacks of any kind.

Let's say you're managing a host called `mash.example.com` which installs both [PeerTube](services/peertube.md) and [NetBox](services/netbox.md). Both of these services require a [Valkey](services/valkey.md) instance. If you simply add `valkey_enabled: true` to your `mash.example.com` host's `vars.yml` file, you'd get a Valkey instance (`mash-valkey`), but it's just one instance. As described in our [Valkey](services/valkey.md) documentation, this is a security problem and potentially fragile as both services may try to read/write the same data and get in conflict with one another.

We propose that you **don't** add `valkey_enabled: true` to your main `mash.example.com` file, but do the following:

## Re-do your inventory to add supplementary hosts

Create multiple hosts in your inventory (`inventory/hosts`) which target the same server, like this:

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com-netbox-deps ansible_host=1.2.3.4
mash.example.com-peertube-deps ansible_host=1.2.3.4
mash.example.com ansible_host=1.2.3.4
```

This creates a new group (called `mash_example_com`) which groups all 3 hosts:

- (**new**) `mash.example.com-netbox-deps` — a new host, for your [NetBox](services/netbox.md) dependencies
- (**new**) `mash.example.com-peertube-deps` — a new host, for your [PeerTube](services/peertube.md) dependencies
- (old) `mash.example.com` — your regular inventory host

When running Ansible commands later on, you can use the `-l` flag to limit which host to run them against. Here are a few examples:

- `just install-all` — runs the [installation](installing.md) process on all hosts (3 hosts in this case)
- `just install-all -l mash_example_com` — runs the installation process on all hosts in the `mash_example_com` group (same 3 hosts as `just install-all` in this case)
- `just install-all -l mash.example.com-netbox-deps` — runs the installation process on the `mash.example.com-netbox-deps` host


## Adjust the configuration of the supplementary hosts to use a new "namespace"

Multiple hosts targetting the same server as described above still causes conflicts, because services will use the same paths (e.g. `/mash/valkey`) and service/container names (`mash-valkey`) everywhere.

To avoid conflicts, adjust the `vars.yml` file for the new hosts (`mash.example.com-netbox-deps` and `mash.example.com-peertube-deps`)
and set non-default and unique values in the `mash_playbook_service_identifier_prefix` and `mash_playbook_service_base_directory_name_prefix` variables. Examples below:

`inventory/host_vars/mash.example.com-netbox-deps/vars.yml`:

```yaml
---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
# Various other secrets will be derived from this secret automatically.
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-netbox-'
mash_playbook_service_base_directory_name_prefix: 'netbox-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################
```

`inventory/host_vars/mash.example.com-peertube-deps/vars.yml`:

```yaml
---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
# Various other secrets will be derived from this secret automatically.
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-peertube-'
mash_playbook_service_base_directory_name_prefix: 'peertube-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################
```

The above configuration will create **2** Valkey instances:

- `mash-netbox-valkey` with its base data path in `/mash/netbox-valkey`
- `mash-peertube-valkey` with its base data path in `/mash/peertube-valkey`

These instances reuse the `mash` user and group and the `/mash` data path, but are not in conflict with each other.


## Adjust the configuration of the base host

Now that we've created separate Valkey instances for both PeerTube and NetBox, we need to put them to use by editing the `vars.yml` file of the main host (the one that installs PeerTbue and NetBox) to wire them to their Valkey instances.

You'll need configuration (`inventory/host_vars/mash.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# netbox                                                               #
#                                                                      #
########################################################################

netbox_enabled: true

# Other NetBox configuration here

# Point NetBox to its dedicated Valkey instance
netbox_environment_variable_redis_host: mash-netbox-valkey
netbox_environment_variable_redis_cache_host: mash-netbox-valkey

# Make sure the NetBox service (mash-netbox.service) starts after its dedicated Valkey service (mash-netbox-valkey.service)
netbox_systemd_required_services_list_custom:
  - mash-netbox-valkey.service

# Make sure the NetBox container is connected to the container network of its dedicated Valkey service (mash-netbox-valkey)
netbox_container_additional_networks_custom:
  - mash-netbox-valkey

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################



########################################################################
#                                                                      #
# peertube                                                             #
#                                                                      #
########################################################################

# Other PeerTube configuration here

# Point PeerTube to its dedicated Valkey instance
peertube_config_redis_hostname: mash-peertube-valkey

# Make sure the PeerTube service (mash-peertube.service) starts after its dedicated Valkey service (mash-peertube-valkey.service)
peertube_systemd_required_services_list_custom:
  - "mash-peertube-valkey.service"

# Make sure the PeerTube container is connected to the container network of its dedicated Valkey service (mash-peertube-valkey)
peertube_container_additional_networks_custom:
  - "mash-peertube-valkey"

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```


## Questions & Answers

**Can't I just use the same Valkey instance for multiple services?**

> You may or you may not. See the [Valkey](services/valkey.md) documentation for why you shouldn't do this.

**Can't I just create one host and a separate stack for each service** (e.g. Nextcloud + all dependencies on one inventory host; PeerTube + all dependencies on another inventory host; with both inventory hosts targetting the same server)?

> That's a possibility which is somewhat clean. The downside is that each "full stack" comes with its own Postgres database which needs to be maintained and upgraded separately.
