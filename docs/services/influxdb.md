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

# Configuring this role for your playbook

influxdb_enabled: true
influxdb_hostname: 'example.org'


# Advanced configuration
# To bootstrap an initial user, bucket and organization you can uncomment and replace

#influxdb_init: true
#influxdb_init_username: "USERNAME"
#influxdb_init_password: "SUPERSECRETPASSWORD"
#influxdb_init_org: "EXAMPLE_ORG"
#influxdb_init_bucket: "SOMEBUCKET"

########################################################################
#                                                                      #
# /influxdb                                                            #
#                                                                      #
########################################################################
```

After installation, visit the domain you set in `influxdb_hostname` to get started.

## Usage

After [installing](../installing.md), you can visit at the URL specified in `influxdb_hostname` and configure your first user (or login if you set `influxdb_init`)
