# immich

[immich](https://github.com/immich-app/immich) is a high performance self-hosted photo and video management solution, that this playbook can install, powered by the [ansible-role-immich](https://github.com/IUCCA/ansible-role-immich) Ansible role.


## Dependencies

This service requires the following other services:
- a [Traefik](traefik.md) reverse-proxy server
- a [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# immich                                                               #
#                                                                      #
########################################################################

immich_enabled: true
immich_hostname: "immich.mash.example.com"
immich_timezone: Europe/Berlin

# immich_hardware_acceleration: cuda

# # Point immich to its dedicated Valkey instance
immich_redis_hostname: mash-immich-valkey

# # Make sure the immich service (mash-immich.service) starts after its dedicated Valkey service (mash-immich-valkey.service)
immich_systemd_required_services_list_custom:
  - "mash-immich-valkey.service"

# # Make sure the immich container is connected to the container network of its dedicated Valkey service (mash-immich-valkey)
immich_container_additional_networks_custom:
  - "mash-immich-valkey"

# # longer timeouts for uploading data to immich
traefik_config_entrypoint_web_transport_respondingTimeouts_readTimeout: 3600s
traefik_config_entrypoint_web_transport_respondingTimeouts_writeTimeout: 3600s
traefik_config_entrypoint_web_transport_respondingTimeouts_idleTimeout: 3600s
########################################################################
#                                                                      #
# /immich                                                              #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://immich.mash.example.com/`.

## Usage

After installation, you can go to the immich URL, as defined in `immich_hostname` and `immich_path_prefix`.

### Valkey

Valkey is required to be enabled.

If immich is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with immich or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [Funkwhale](funkwhale.md), and [SearXNG](searxng.md)), it is recommended to install a Valkey instance dedicated to immich.

#### Setting up a dedicated Valkey instance

To create a dedicated instance for immich, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for immich.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-immich-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-immich-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-immich-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-immich-valkey` instance on the new host, setting `/mash/immich-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of immich.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-immich-'
mash_playbook_service_base_directory_name_prefix: 'immich-'

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