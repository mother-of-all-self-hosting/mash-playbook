# InfluxDB

[InfluxDB](https://www.influxdata.com/) is a self-hosted time-series database, that this playbook can install, powered by the [mother-of-all-self-hosting/ansible-role-influxdb](https://github.com/mother-of-all-self-hosting/ansible-role-influxdb) Ansible role.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# influxdb                                                             #
#                                                                      #
########################################################################

influxdb_enabled: true
influxdb_hostname: 'example.org'

# Advanced configuration
# Configure the initial user, organization and bucket
#
# This setting will only be used once upon initial installation of influxdb. Changing this values
# after the first start of influxdb will have no effect.
# Not setting this will allow you to manually set these by visiting the domain you set in influxdb_hostname
# after installation.
#influxdb_init: true
#influxdb_init_username: "USERNAME"
#influxdb_init_password: "SUPERSECRETPASSWORD"
#influxdb_init_org: "EXAMPLE_ORG"
#influxdb_init_bucket: "SOMEBUCKET"
#
# In order to let external services (like Proxmox or Grafana) access the http API of influxdb,
# you need to specifically expose the corresponding port:
#
# Takes an "<ip>:<port>" (e.g. "127.0.0.1:8086") or "<port>" value (e.g. "8086"), or empty string to not expose.
#influxdb_container_http_host_bind_port: ""

########################################################################
#                                                                      #
# /influxdb                                                            #
#                                                                      #
########################################################################
```

After installation, visit the domain you set in `influxdb_hostname` to get started.

## Usage

After [installing](../installing.md), you can visit at the URL specified in `influxdb_hostname` and configure your first user (or login if you set `influxdb_init`)
