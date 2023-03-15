# Miniflux

[Garage](https://garagehq.deuxfleurs.fr/) is an open-source distributed object storage service tailored for self-hosting.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file, adjust it to your needs and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# garage                                                               #
#                                                                      #
########################################################################

# Garage uses a secret key that is shared between all nodes of the cluster in order to identify these nodes and allow
# them to communicate together. This key should be specified here in the form of a 32-byte hex-encoded random string.
# Such a string can be generated with a command such as ´openssl rand -hex 32´.
garage_rpc_secret: 'verysecret'

# Token for accessing the admin API.
# Generating a strong secret is advised (e.g. `openssl rand -hex 32`).
garage_admin_token: 'verysecret'

# This is the zone that your host will be in. Refer to https://garagehq.deuxfleurs.fr/documentation/cookbook/real-world/#creating-a-cluster-layout
# for more information
garage_zone: "dc1"

# The replication mode defines how many copies of your data are stored per region
# "2" means data stored on Garage will be stored on two different nodes, if possible in different zones. Adjust this
# to your needs.
# Full reference: https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/#replication-mode
garage_replication_mode: 2


########################
## NODE CONFIGURATION ##
########################

# This is an example configuration of nodes. On this host we run 2 data nodes that both manage 1 3TB drive.
# We access the nodes via a gateway node.

garage_node1_base_path: "/media/drive1/garage/node1"
garage_node2_base_path: "/media/drive2/garage/node2"
garage_nodes:
  - name: "gateway1"
    metadata_path: "{{ garage_meta_path }}/gw1"
    data_path: "{{ garage_data_path }}/gw1"
    gateway: true
    rpc_bind_port: 3901
    node_addr: "garage-gw1.example.com"
    s3_api_addr: "s3.example.com"
  - name: "node1"
    gateway: false
    capacity: 3
    metadata_path: "{{ garage_node1_base_path }}/metadata"
    data_path: "{{ garage_node1_base_path }}/data"
    rpc_bind_port: 3911
    node_addr: "garage-node1.example.com"
  - name: "node2"
    gateway: false
    capacity: 3
    metadata_path: "{{ garage_node2_base_path }}/metadata"
    data_path: "{{ garage_node2_base_path }}/data"
    rpc_bind_port: 3921
    node_addr: "garage-node2.example.com"

########################################################################
#                                                                      #
# /garage                                                              #
#                                                                      #
########################################################################
```

## Usage

After installation, you should run
```
ansible-playbook -i inventory/hosts setup.yml --tags=configure-garage
```
to connect the nodes and apply the layout.

Then you can create your first bucket with 
```
ansible-playbook -i inventory/hosts setup.yml --tags=create-bucket --extra-vars "bucket=<bucketname>"
```
and get an access key for it with
```
ansible-playbook -i inventory/hosts setup.yml --tags=create-bucket --extra-key "bucket=<bucketname> keyname=<keyname>"
```

arage is very versatile so make sure to check out the [documentation](https://garagehq.deuxfleurs.fr/documentation/quick-start/). You can always execute you own commands by ssh-ing to the server and running

```
docker exec -it <any_node_name> /garage <command>
```
