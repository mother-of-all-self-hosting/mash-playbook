<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# InfluxDB

The playbook can install and configure [InfluxDB](https://www.influxdata.com/) for you.

InfluxDB is a self-hosted time-series database.

See the project's [documentation](https://github.com/docker-library/docs/blob/master/influxdb/README.md) to learn what InfluxDB does and why it might be useful to you.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# influxdb                                                             #
#                                                                      #
########################################################################

influxdb_enabled: true
influxdb_hostname: influxdb.example.com

########################################################################
#                                                                      #
# /influxdb                                                            #
#                                                                      #
########################################################################
```

### Configure the initial user (optional)

You can set up the initial user by adding the following configuration to your `vars.yml` file:

```yaml
influxdb_init: true
influxdb_init_username: YOUR_USERNAME_HERE
influxdb_init_password: YOUR_PASSWORD_HERE
influxdb_init_org: YOUR_EXAMPLE_ORG_HERE
influxdb_init_bucket: YOUR_BUCKET_HERE
```

>[!NOTE]
> The settings will only be used once upon initial installation of InfluxDB. Changing these values after the first start of it will have no effect.

Not setting them allows you to create the user manually after installation by visiting the hostname set to `influxdb_hostname`.

### Expose the port for external services (optional)

In order to let external services (like Proxmox or Grafana) access the InfluxDB's HTTP API, the corresponding port needs to be exposed.

```yaml
influxdb_container_http_host_bind_port: PORT_NUMBER_HERE
```

## Usage

After running the command for installation, InfluxDB becomes available at the specified hostname like `https://influxdb.example.com`.

You can go to the URL with a web browser to log in if `influxdb_init` is set to `true` (or configure the first user if it is not).
